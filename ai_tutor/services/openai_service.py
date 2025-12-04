import os
import openai
from django.conf import settings

# Configure API key from environment or Django settings
openai.api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)


def _mock_response(message: str, exercise, user_query: str = None, error: str = None) -> str:
    """Return a short canned response for demo/mock mode."""
    ex_title = getattr(exercise, 'title', 'this exercise') if exercise is not None else 'the exercise'
    # Keep response concise to save tokens in eventual real mode
    if error:
        return f"I see an error: {error}. Check your SELECT columns and WHERE clause for typos. (mock)"
    if user_query:
        return f"Your query looks reasonable for {ex_title}. Consider ordering results or selecting explicit columns. (mock)"
    return f"Try selecting the relevant columns from the table for {ex_title}. (mock)"


def get_ai_response(message: str, exercise=None, user_query: str = None, error: str = None) -> str:
    """Get AI tutor response.

    Behavior:
    - If `OPENAI_MODE` in Django settings is 'mock' (default), return a canned response.
    - If set to 'real', attempt a single short OpenAI chat completion call (with token limits).
    """
    mode = getattr(settings, 'OPENAI_MODE', 'mock')
    # Mock mode: quick, deterministic, zero-cost
    if mode != 'real':
        return _mock_response(message, exercise, user_query, error)

    # Real mode: attempt to call OpenAI with strict limits
    if not openai.api_key:
        return "AI tutor is not configured (missing OPENAI_API_KEY)."

    prompt = f"You are a concise SQL tutor. Message: {message}\nExercise: {getattr(exercise, 'title', None)}\nUser query: {user_query}\nError: {error}"
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "You are a concise SQL tutor. Keep responses short and focused."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.2,
        )
        # Safe access to response
        choices = getattr(resp, 'choices', None) or resp.get('choices', [])
        if choices:
            # openai library response shape may vary; handle common patterns
            content = choices[0].get('message', {}).get('content') if isinstance(choices[0], dict) else getattr(choices[0].message, 'content', '')
            return (content or '').strip()
        return "AI returned no content."
    except Exception:
        return "AI tutor failed to generate a response (see server logs)."
