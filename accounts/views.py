from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import UserProfile


def check_instructor(user):
    """检查用户是否是 instructor"""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.role == 'instructor'


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'student')

    if not username or not password:
        return Response({'error': 'Username and password required'},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    if role not in ['student', 'instructor']:
        return Response({'error': 'Invalid role. Must be "student" or "instructor"'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        password=make_password(password)
    )
    
    user.profile.role = role
    user.profile.save()

    return Response({
        'message': 'User created successfully',
        'username': user.username,
        'role': user.profile.role
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid username or password'},
                        status=status.HTTP_401_UNAUTHORIZED)

    auth_login(request, user)

    return Response({
        "message": "Login successful",
        "username": username,
        "role": user.profile.role,
        "userId": user.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    if not request.user.is_authenticated:
        return Response(
            {"error": "User is not logged in"},
            status=status.HTTP_400_BAD_REQUEST
        )

    auth_logout(request)
    return Response(
        {"message": "Logout successful"},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def me(request):
    if request.user.is_authenticated:
        return Response({
            "authenticated": True,
            "username": request.user.username,
            "role": request.user.profile.role,
            "userId": request.user.id
        }, status=status.HTTP_200_OK)

    return Response(
        {"authenticated": False},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "username": request.user.username,
        "role": request.user.profile.role,
        "message": "This is a protected endpoint",
    }, status=status.HTTP_200_OK)


# ============================================
# Instructor APIs
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_stats(request):
    """GET /api/instructor/stats/"""
    
    if not check_instructor(request.user):
        return Response({'error': 'Unauthorized'}, status=403)
    
    from exercises.models import Exercise, Submission
    
    total_students = User.objects.filter(profile__role='student').count()
    total_exercises = Exercise.objects.count()
    total_submissions = Submission.objects.count()
    
    if total_submissions > 0:
        correct_submissions = Submission.objects.filter(status='correct').count()
        avg_completion_rate = round((correct_submissions / total_submissions) * 100, 1)
    else:
        avg_completion_rate = 0
    
    return Response({
        'total_students': total_students,
        'total_exercises': total_exercises,
        'total_submissions': total_submissions,
        'average_completion_rate': avg_completion_rate
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_students(request):
    """GET /api/instructor/students/"""
    
    if not check_instructor(request.user):
        return Response({'error': 'Unauthorized'}, status=403)
    
    students = User.objects.filter(profile__role='student').annotate(
        submissions_count=Count('submissions')
    ).order_by('-date_joined')
    
    data = [{
        'id': s.id,
        'username': s.username,
        'student_id': str(s.profile.student_id)[:8].upper() if s.profile.student_id else f"STU{s.id:06d}",
        'date_joined': s.date_joined,
        'last_login': s.last_login,
        'submissions_count': s.submissions_count
    } for s in students]

    print("DEBUG - First student:", data[0] if data else "No students")
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_student_detail(request, student_id):
    """GET /api/instructor/students/{id}/"""
    
    if not check_instructor(request.user):
        return Response({'error': 'Unauthorized'}, status=403)
    
    from exercises.models import Submission
    
    student = get_object_or_404(User, id=student_id, profile__role='student')
    
    submissions = Submission.objects.filter(user=student).select_related('exercise').order_by('-created_at')[:20]
    
    data = {
        'id': student.id,
        'username': student.username,
        'student_id': str(student.profile.student_id)[:8].upper() if student.profile.student_id else f"STU{student.id:06d}",
        'date_joined': student.date_joined,
        'last_login': student.last_login,
        'submissions': [{
            'id': sub.id,
            'exercise_title': sub.exercise.title,
            'status': sub.status,
            'created_at': sub.created_at,
        } for sub in submissions]
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_recent_activity(request):
    """GET /api/instructor/recent-activity/"""
    
    if not check_instructor(request.user):
        return Response({'error': 'Unauthorized'}, status=403)
    
    from exercises.models import Submission
    
    recent_submissions = Submission.objects.select_related(
        'user', 'exercise'
    ).order_by('-created_at')[:20]
    
    data = [{
        'id': sub.id,
        'user': sub.user.username,
        'action': f'Submitted answer to "{sub.exercise.title}"',
        'date': sub.created_at,
        'status': sub.status
    } for sub in recent_submissions]
    
    return Response(data)