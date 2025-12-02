from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from exercises.models import Exercise, ChatHistory
from ai_tutor.services.openai_service import get_ai_response


class ExerciseAIView(APIView):
    """POST /api/exercises/{id}/ai/ - Get AI help (mock or real depending on settings)"""

    def post(self, request, exercise_id):
        exercise = get_object_or_404(Exercise, id=exercise_id)
        message = request.data.get('message', '')
        user_query = request.data.get('user_query')
        error = request.data.get('error')

        if not message and not user_query and not error:
            return Response({'error': 'message or user_query or error is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure session
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        # Get AI response (mock or real)
        resp_text = get_ai_response(message or user_query or 'Help me', exercise, user_query, error)

        # Persist ChatHistory
        ChatHistory.objects.create(
            session_id=session_id,
            exercise=exercise,
            message=message or user_query or '',
            response=resp_text,
            context={'user_query': user_query, 'error': error}
        )

        return Response({'response': resp_text})
