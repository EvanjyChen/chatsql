from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import connection
from exercises.models import Exercise, ChatHistory
from ai_tutor.services.openai_service import get_ai_response

@method_decorator(csrf_exempt, name='dispatch')
class ExerciseAIView(APIView):
    """POST /api/exercises/{id}/ai/ - Get AI help for students"""
    # permission_classes = [IsAuthenticated]

    def post(self, request, exercise_id):
        exercise = get_object_or_404(Exercise, id=exercise_id)
        message = request.data.get('message', '')
        user_query = request.data.get('user_query')
        error = request.data.get('error')

        if not message and not user_query and not error:
            return Response(
                {'error': 'message or user_query or error is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 临时修复：使用假 user_id 或从 session 获取
        user_id = request.user.id if request.user.is_authenticated else 1

        # Ensure session
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        # Get AI response (returns dict with sql_query, should_execute, etc.)
        ai_result = get_ai_response(
            message=message or user_query or 'Help me',
            exercise=exercise,
            user_query=user_query,
            error=error,
            user_role='student',  # Hard-coded for now, will use request.user.role later
            user_id=user_id
        )

        response_data = {
            'response': ai_result['response'],
            'intent': ai_result['intent']
        }

        # If AI generated SQL and wants to execute it
        if ai_result['should_execute'] and ai_result['sql_query']:
            try:
                # Execute the AI-generated SQL
                execution_result = self._execute_sql(ai_result['sql_query'])
                
                response_data['sql_query'] = ai_result['sql_query']
                response_data['query_result'] = execution_result
                response_data['executed'] = True
                
                # Append result to response text
                result_summary = self._format_result_summary(execution_result)
                response_data['response'] = f"{ai_result['response']}\n\n{result_summary}"
                
            except Exception as e:
                response_data['sql_query'] = ai_result['sql_query']
                response_data['execution_error'] = str(e)
                response_data['executed'] = False
                response_data['response'] = f"{ai_result['response']}\n\n⚠️ Failed to execute query: {str(e)}"
        
        elif ai_result['sql_query'] and not ai_result['should_execute']:
            # SQL generated but not auto-executed (e.g., for teaching purposes)
            response_data['sql_query'] = ai_result['sql_query']
            response_data['executed'] = False

        # Persist ChatHistory
        ChatHistory.objects.create(
            session_id=session_id,
            exercise=exercise,
            message=message or user_query or '',
            response=response_data['response'],
            context={
                'user_query': user_query,
                'error': error,
                'ai_generated_sql': ai_result.get('sql_query'),
                'intent': ai_result['intent']
            }
        )

        return Response(response_data)

    def _execute_sql(self, sql_query: str) -> dict:
        """Execute SQL query and return results."""
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            
            # Check if it's a SELECT query
            if sql_query.strip().upper().startswith('SELECT'):
                columns = [col[0] for col in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                return {
                    'success': True,
                    'columns': columns,
                    'rows': [list(row) for row in rows],
                    'row_count': len(rows)
                }
            else:
                # UPDATE/INSERT/DELETE
                return {
                    'success': True,
                    'affected_rows': cursor.rowcount,
                    'message': f'{cursor.rowcount} row(s) affected'
                }

    def _format_result_summary(self, result: dict) -> str:
        """Format query result into readable text."""
        if not result['success']:
            return "❌ Query execution failed"
        
        if 'rows' in result:
            # SELECT result
            count = result['row_count']
            if count == 0:
                return "📊 Query executed successfully (0 results)"
            elif count == 1:
                return f"📊 Query returned 1 result"
            else:
                return f"📊 Query returned {count} results"
        else:
            # UPDATE/INSERT/DELETE result
            return f"✅ {result['message']}"