"""
API authentication endpoints (login, logout, register)
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from accounts.forms import UserRegistrationForm
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_register(request):
    """
    Register a new user via API
    POST /api/auth/register/
    {
        "username": "user",
        "email": "user@example.com",
        "password1": "SecurePass123",
        "password2": "SecurePass123",
        "bio": "Optional bio"
    }
    """
    form = UserRegistrationForm(request.data)
    
    if form.is_valid():
        user = form.save()
        logger.info(f"User registered via API: {user.username}")
        
        # Automatically log in the user
        login(request, user)
        
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    else:
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = field_errors
        return Response({
            'error': 'VALIDATION_ERROR',
            'message': 'Registration failed',
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    """
    Login via API
    POST /api/auth/login/
    {
        "username": "user",
        "password": "password123"
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'VALIDATION_ERROR',
            'message': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        logger.info(f"User logged in via API: {user.username}")
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Failed login attempt via API: {username}")
        return Response({
            'error': 'AUTHENTICATION_FAILED',
            'message': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_logout(request):
    """
    Logout via API
    POST /api/auth/logout/
    Requires authentication
    """
    username = request.user.username
    logout(request)
    logger.info(f"User logged out via API: {username}")
    
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_user_info(request):
    """
    Get current user information
    GET /api/auth/user/
    Requires authentication
    """
    return Response({
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)

