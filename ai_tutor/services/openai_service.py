import os
import re
from django.conf import settings
from openai import OpenAI

# Configure API key
API_KEY = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)


def _mock_response(message: str, exercise, user_query: str = None, error: str = None) -> dict:
    """Return a short canned response for demo/mock mode."""
    ex_title = getattr(exercise, 'title', 'this exercise') if exercise is not None else 'the exercise'
    
    # Detect if message looks like a data query
    query_keywords = ['how many', 'show me', 'find', 'list', 'count', 'what is my', 'my progress', 'did i solve']
    is_data_query = any(keyword in message.lower() for keyword in query_keywords)
    
    if is_data_query:
        # Mock SQL generation and execution
        return {
            'response': "Based on your question, here's what I found: You have completed 3 exercises this month. (mock data)",
            'sql_query': "SELECT COUNT(*) FROM submissions WHERE user_id=1 AND status='correct' AND MONTH(created_at)=MONTH(CURRENT_DATE)",
            'should_execute': True,
            'intent': 'data_query'
        }
    
    # Regular tutoring response
    if error:
        response_text = f"I see an error: {error}. Check your SELECT columns and WHERE clause for typos."
    elif user_query:
        response_text = f"Your query looks reasonable for {ex_title}. Consider ordering results or selecting explicit columns."
    else:
        response_text = f"Try selecting the relevant columns from the table for {ex_title}."
    
    return {
        'response': response_text,
        'sql_query': None,
        'should_execute': False,
        'intent': 'tutoring'
    }


def _build_student_prompt(user_id: int) -> str:
    """Build student-specific system prompt."""
    
    return f"""You are an intelligent SQL tutor assistant for students. Analyze the user's message and determine the intent:

**Intent Types:**
1. DATA_QUERY - User wants to check their own statistics/progress
2. TUTORING - User needs explanation of SQL concepts
3. DEBUG - User needs help fixing their query

**For DATA_QUERY:**
- Generate executable SQL to query the student's data
- Mark response with [SQL_QUERY] tag
- Include brief explanation
- Always filter by user_id={user_id}

**For TUTORING/DEBUG:**
- Provide clear, concise explanation
- Give examples when helpful
- No SQL generation needed

**Available tables:**
- exercises: (id, title, description, difficulty, workshop, database_name)
- submissions: (id, user_id, exercise_id, query, status, created_at)
  - status values: 'correct', 'incorrect', 'pending'

**Student can query:**
- Their submission history
- Their progress statistics  
- Problems they haven't solved
- Their performance over time

**Examples:**

User: "How many problems did I solve this month?"
Response:
[SQL_QUERY]
SELECT COUNT(*) FROM submissions 
WHERE user_id={user_id} 
AND status='correct' 
AND MONTH(created_at) = MONTH(CURRENT_DATE)
AND YEAR(created_at) = YEAR(CURRENT_DATE)

This counts your correct submissions from the current month.

---

User: "What's the difference between INNER JOIN and LEFT JOIN?"
Response:
INNER JOIN returns only matching rows from both tables, while LEFT JOIN returns all rows from the left table and matching rows from the right table (with NULLs for non-matches).

Example:
- INNER JOIN: Only students with submissions
- LEFT JOIN: All students, even those without submissions
"""


def _extract_sql_from_response(response_text: str) -> tuple[str, str]:
    """Extract SQL query and intent from AI response."""
    
    # Check for SQL marker
    if '[SQL_QUERY]' not in response_text:
        return None, 'tutoring'
    
    # Extract SQL (look for SELECT/UPDATE/INSERT)
    sql_pattern = r'(SELECT|UPDATE|INSERT|DELETE)\s+[\s\S]*?(?=\n\n|\Z)'
    match = re.search(sql_pattern, response_text, re.IGNORECASE | re.MULTILINE)
    
    if match:
        sql_query = match.group(0).strip()
        # Clean up markdown formatting
        sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        # Remove trailing explanation
        sql_query = sql_query.split('\n\n')[0].strip()
        return sql_query, 'data_query'
    
    return None, 'tutoring'


def get_ai_response(
    message: str, 
    exercise=None, 
    user_query: str = None, 
    error: str = None,
    user_role: str = 'student',
    user_id: int = None
) -> dict:
    """Get AI tutor response for students with SQL generation capability.
    
    Returns dict:
    {
        'response': str,
        'sql_query': str | None,
        'should_execute': bool,
        'intent': str
    }
    """
    mode = getattr(settings, 'OPENAI_MODE', 'mock')
    
    # Mock mode
    if mode != 'real':
        return _mock_response(message, exercise, user_query, error)
    
    # Real mode
    if not API_KEY:
        return {
            'response': "AI tutor is not configured (missing OPENAI_API_KEY).",
            'sql_query': None,
            'should_execute': False,
            'intent': 'error'
        }
    
    if not user_id:
        return {
            'response': "User ID is required for AI assistance.",
            'sql_query': None,
            'should_execute': False,
            'intent': 'error'
        }
    
    # Build student prompt
    system_prompt = _build_student_prompt(user_id)
    
    # Build user message with context
    user_prompt = f"User message: {message}"
    if exercise:
        user_prompt += f"\nCurrent exercise: {getattr(exercise, 'title', None)}"
        user_prompt += f"\nDifficulty: {getattr(exercise, 'difficulty', None)}"
    if user_query:
        user_prompt += f"\nStudent's SQL attempt: {user_query}"
    if error:
        user_prompt += f"\nExecution error: {error}"
    
    try:
        # Create OpenAI client
        client = OpenAI(api_key=API_KEY)
        
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.3,
        )
        
        # Extract response
        if not response.choices:
            return {
                'response': "AI returned no content.",
                'sql_query': None,
                'should_execute': False,
                'intent': 'error'
            }
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse response for SQL and intent
        sql_query, intent = _extract_sql_from_response(response_text)
        
        # Replace user_id placeholder if present
        if sql_query and '{user_id}' in sql_query:
            sql_query = sql_query.replace('{user_id}', str(user_id))
        
        # Auto-execute data queries
        should_execute = (intent == 'data_query' and sql_query is not None)
        
        return {
            'response': response_text,
            'sql_query': sql_query,
            'should_execute': should_execute,
            'intent': intent
        }
        
    except Exception as e:
        return {
            'response': f"AI tutor encountered an error: {str(e)}. Please try rephrasing your question.",
            'sql_query': None,
            'should_execute': False,
            'intent': 'error'
        }