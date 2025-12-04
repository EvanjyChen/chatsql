from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import models as dj_models
from django.utils import timezone
from .models import DatabaseSchema, Exercise, UserProgress
from .services.executor import SQLExecutor
import uuid
import re
import pymysql
from django.db import connection
from django.conf import settings

def get_db_name_for_exercise(exercise):
    """
    根据题目标题提取 WS 编号，返回对应的数据库名
    例如: "WS1-1: ..." -> "WS1", "WS2-3: ..." -> "WS2"
    如果无法提取，则使用 schema.db_name
    """
    # 从标题中提取 WS 编号（如 WS1, WS2, WS10, WS11）
    match = re.match(r'WS(\d+)', exercise.title)
    if match:
        ws_num = match.group(1)
        db_name = f'WS{ws_num}'
        # 检查该数据库是否在 settings.DATABASES 中配置
        if db_name in settings.DATABASES:
            return db_name
    
    # 如果无法提取或数据库不存在，使用 schema.db_name
    return exercise.schema.db_name

def fix_table_names_in_sql(sql, db_name):
    """
    尝试修复 SQL 中的表名大小写问题
    通过查询数据库获取实际表名，然后替换 SQL 中的表名
    """
    if db_name not in settings.DATABASES:
        return sql
    
    db_config = settings.DATABASES[db_name]
    host = db_config.get('HOST')
    user = db_config.get('USER')
    password = db_config.get('PASSWORD')
    database = db_config.get('NAME')
    port = int(db_config.get('PORT', 3306))
    
    if not all([host, user, password, database]):
        return sql
    
    try:
        # 连接到数据库获取实际表名
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=2
        )
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            actual_tables = {row[0].lower(): row[0] for row in cursor.fetchall()}
        conn.close()
        
        # 替换 SQL 中的表名
        def replace_table_name(match):
            table_name = match.group(0)
            table_lower = table_name.lower()
            if table_lower in actual_tables:
                return actual_tables[table_lower]
            return table_name
        
        # 匹配 SQL 中的表名（考虑引号、反引号等）
        # 匹配 FROM, JOIN, UPDATE, INSERT INTO, DELETE FROM 后的表名
        pattern = r'\b(?:FROM|JOIN|UPDATE|INTO|TABLE)\s+[`"]?(\w+)[`"]?'
        fixed_sql = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), actual_tables.get(m.group(1).lower(), m.group(1))), sql, flags=re.IGNORECASE)
        
        return fixed_sql
    except Exception:
        # 如果无法连接或修复失败，返回原始 SQL
        return sql

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
    """
    GET /api/exercises/
    支持的筛选参数（全部可选）：
      - schema_id: 按 schema 过滤
      - difficulty: 难度（easy/medium/hard）
      - search: 关键字，模糊匹配 title / description / tags
    """
    
    def get(self, request):
        exercises = Exercise.objects.select_related('schema').all()
        
        # 动态拼接 filter 条件
        filters = {}
        
        # Filter by schema
        schema_id = request.query_params.get('schema_id')
        if schema_id:
            filters['schema_id'] = schema_id
        
        # Filter by difficulty
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            filters['difficulty'] = difficulty
        
        if filters:
            exercises = exercises.filter(**filters)
        
        # 关键字搜索（动态 SQL 条件：使用 Q 对象组合）
        search = request.query_params.get('search')
        if search:
            exercises = exercises.filter(
                dj_models.Q(title__icontains=search) |
                dj_models.Q(description__icontains=search) |
                dj_models.Q(tags__icontains=search)
            )
        
        # 确保按照 order 字段排序（从小到大），order 相同时按 id 排序
        exercises = exercises.order_by('order', 'id')
        
        data = [{
            'id': ex.id,
            'title': ex.title,
            'difficulty': ex.difficulty,
            'order': ex.order,  # 包含 order 字段，用于前端排序
            'schema': {
                'id': ex.schema.id,
                'name': ex.schema.name,
                'display_name': ex.schema.display_name,
            },
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
                'db_name': get_db_name_for_exercise(exercise)  # 使用根据题目标题确定的数据库名
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
        # 根据题目标题选择对应的 WS 数据库
        db_name = get_db_name_for_exercise(exercise)
        try:
            executor = SQLExecutor(db_name)
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
        # 根据题目标题选择对应的 WS 数据库
        db_name = get_db_name_for_exercise(exercise)
        executor = None
        try:
            executor = SQLExecutor(db_name)
            user_result = executor.execute(query)
            # 尝试修复期望 SQL 中的表名大小写问题
            fixed_expected_sql = fix_table_names_in_sql(exercise.expected_sql, db_name)
            expected_result = executor.execute(fixed_expected_sql)
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
            # 创建临时 executor 用于比较结果
            executor = SQLExecutor(db_name) if db_name in settings.DATABASES else None
        
        # Compare results
        if executor:
            comparison = executor.compare_results(user_result, expected_result)
        else:
            # 如果无法创建 executor，进行简单比较
            comparison = {
                'correct': user_result['success'] and expected_result['success'] and 
                          user_result.get('row_count') == expected_result.get('row_count'),
                'message': 'Results compared (fallback mode)' if user_result['success'] and expected_result['success'] else 'Query execution failed'
            }
        
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
