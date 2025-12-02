from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import models as dj_models
from django.utils import timezone
from .models import DatabaseSchema, Exercise, UserProgress
from .services.executor import SQLExecutor
import uuid
from django.db import connection

class SchemaListView(APIView):
    """GET /api/schemas/ - List all database schemas"""
    
    def get(self, request):
        schemas = DatabaseSchema.objects.all()
        data = [{
            'id': s.id,
            'name': s.name,
            'display_name': s.display_name,
            'description': s.description,
            'exercise_count': s.exercises.count()
        } for s in schemas]
        return Response(data)

class ExerciseListView(APIView):
    """GET /api/exercises/?schema_id=1&difficulty=easy"""
    
    def get(self, request):
        exercises = Exercise.objects.select_related('schema').all()
        
        # Filter by schema
        schema_id = request.query_params.get('schema_id')
        if schema_id:
            exercises = exercises.filter(schema_id=schema_id)
        
        # Filter by difficulty
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            exercises = exercises.filter(difficulty=difficulty)
        
        data = [{
            'id': ex.id,
            'title': ex.title,
            'difficulty': ex.difficulty,
            'schema': ex.schema.display_name,
            'tags': ex.tags,
            'completed': False  # TODO: Check user progress
        } for ex in exercises]
        
        return Response(data)

class ExerciseDetailView(APIView):
    """GET /api/exercises/{id}/ - Get exercise details"""
    
    def get(self, request, exercise_id):
        exercise = get_object_or_404(Exercise.objects.select_related('schema'), id=exercise_id)
        
        data = {
            'id': exercise.id,
            'title': exercise.title,
            'description': exercise.description,
            'difficulty': exercise.difficulty,
            'initial_query': exercise.initial_query or f"SELECT \n  -- Write your query here\nFROM ",
            'hints': exercise.hints,
            'schema': {
                'id': exercise.schema.id,
                'name': exercise.schema.name,
                'display_name': exercise.schema.display_name,
                'db_name': exercise.schema.db_name
            },
            'tags': exercise.tags
        }
        
        return Response(data)

class ExecuteQueryView(APIView):
    """POST /api/exercises/{id}/execute/ - Execute user query"""
    
    def post(self, request, exercise_id):
        exercise = get_object_or_404(Exercise.objects.select_related('schema'), id=exercise_id)
        query = request.data.get('query', '').strip()
        
        if not query:
            return Response(
                {'error': 'Query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Execute query using SQLExecutor if configured, otherwise run against default DB
        try:
            executor = SQLExecutor(exercise.schema.db_name)
            result = executor.execute(query)
        except ValueError:
            # Fallback: execute against default DB (SQLite) using Django connection
            start = timezone.now()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchmany(SQLExecutor.MAX_ROWS)
                    columns = [col[0] for col in cursor.description] if cursor.description else []
                    row_list = [list(row) for row in rows]
                exec_time = (timezone.now() - start).total_seconds()
                result = {
                    'success': True,
                    'columns': columns,
                    'rows': row_list,
                    'row_count': len(row_list),
                    'execution_time': round(exec_time, 3),
                    'error': None
                }
            except Exception as e:
                exec_time = (timezone.now() - start).total_seconds()
                result = {
                    'success': False,
                    'error': str(e),
                    'columns': [],
                    'rows': [],
                    'row_count': 0,
                    'execution_time': round(exec_time, 3)
                }
        
        # Track attempt (get or create session)
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        # Update or create progress: increment attempts if exists, else create with attempts=1
        try:
            up = UserProgress.objects.get(session_id=session_id, exercise=exercise)
            up.last_query = query
            up.attempts = dj_models.F('attempts') + 1
            up.save(update_fields=['last_query', 'attempts'])
        except UserProgress.DoesNotExist:
            UserProgress.objects.create(session_id=session_id, exercise=exercise, last_query=query, attempts=1)
        
        return Response(result)

class SubmitQueryView(APIView):
    """POST /api/exercises/{id}/submit/ - Submit and validate query"""
    
    def post(self, request, exercise_id):
        exercise = get_object_or_404(Exercise.objects.select_related('schema'), id=exercise_id)
        query = request.data.get('query', '').strip()
        
        if not query:
            return Response(
                {'error': 'Query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Execute both user query and expected query, with fallback to default DB
        try:
            executor = SQLExecutor(exercise.schema.db_name)
            user_result = executor.execute(query)
            expected_result = executor.execute(exercise.expected_sql)
        except ValueError:
            # Fallback execution on default DB
            def run_on_default(q):
                start = timezone.now()
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(q)
                        rows = cursor.fetchmany(SQLExecutor.MAX_ROWS)
                        columns = [col[0] for col in cursor.description] if cursor.description else []
                        row_list = [list(row) for row in rows]
                    exec_time = (timezone.now() - start).total_seconds()
                    return {
                        'success': True,
                        'columns': columns,
                        'rows': row_list,
                        'row_count': len(row_list),
                        'execution_time': round(exec_time, 3),
                        'error': None
                    }
                except Exception as e:
                    exec_time = (timezone.now() - start).total_seconds()
                    return {
                        'success': False,
                        'error': str(e),
                        'columns': [],
                        'rows': [],
                        'row_count': 0,
                        'execution_time': round(exec_time, 3)
                    }

            user_result = run_on_default(query)
            expected_result = run_on_default(exercise.expected_sql)
        
        # Compare results
        comparison = executor.compare_results(user_result, expected_result)
        
        # Update progress
        session_id = request.session.session_key or str(uuid.uuid4())
        
        if comparison['correct']:
            UserProgress.objects.update_or_create(
                session_id=session_id,
                exercise=exercise,
                defaults={
                    'completed': True,
                    'last_query': query,
                    'completed_at': timezone.now()
                }
            )
        
        return Response({
            'correct': comparison['correct'],
            'message': comparison['message'],
            'user_result': user_result,
            'diff': comparison.get('diff')
        })
