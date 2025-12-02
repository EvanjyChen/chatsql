from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Simple validation (to prevent empty fields)
    if not username or not password:
        return Response({'error': 'Username and password required'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check if the username already exists.
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Create a user (automatically hash the password)
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )

    return Response({'message': 'User created successfully', 'username': user.username},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check credentials
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid username or password'},
                        status=status.HTTP_401_UNAUTHORIZED)

    # Attach session to this user
    auth_login(request, user)

    return Response(
        {
            "message": "Login successful",
            "username": username,
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def logout_view(request):
    # If user is not logged in, return error
    if not request.user.is_authenticated:
        return Response(
            {"error": "User is not logged in"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # If logged in, clear session
    auth_logout(request)
    return Response(
        {"message": "Logout successful"},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def me(request):
    if request.user.is_authenticated:
        return Response(
            {
                "authenticated": True,
                "username": request.user.username,
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {"authenticated": False},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(
        {
            "username": request.user.username,
            "message": "This is a protected endpoint",
        },
        status=status.HTTP_200_OK
    )
