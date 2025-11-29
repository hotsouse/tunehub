"""
Global exception handling for API
"""
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns structured error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it means it's an unhandled exception
    if response is None:
        # Handle Django-specific exceptions
        if isinstance(exc, Http404):
            response_data = {
                'error': 'NOT_FOUND',
                'message': str(exc) or 'Resource not found',
                'status_code': status.HTTP_404_NOT_FOUND
            }
            logger.warning(f"404 Not Found: {exc}", exc_info=True)
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        elif isinstance(exc, PermissionDenied):
            response_data = {
                'error': 'PERMISSION_DENIED',
                'message': 'You do not have permission to perform this action',
                'status_code': status.HTTP_403_FORBIDDEN
            }
            logger.warning(f"403 Permission Denied: {exc}", exc_info=True)
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        elif isinstance(exc, ValidationError):
            response_data = {
                'error': 'VALIDATION_ERROR',
                'message': str(exc),
                'status_code': status.HTTP_400_BAD_REQUEST
            }
            logger.warning(f"400 Validation Error: {exc}", exc_info=True)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exc, IntegrityError):
            response_data = {
                'error': 'INTEGRITY_ERROR',
                'message': 'Database integrity constraint violated',
                'status_code': status.HTTP_409_CONFLICT
            }
            logger.error(f"409 Integrity Error: {exc}", exc_info=True)
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        
        # Generic 500 error for unhandled exceptions
        logger.error(f"500 Internal Server Error: {exc}", exc_info=True, extra={'context': context})
        response_data = {
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'An internal server error occurred',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        # In production, don't expose error details
        from django.conf import settings
        if not settings.DEBUG:
            response_data['message'] = 'An error occurred. Please try again later.'
        
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Customize the response data structure
    custom_response_data = {
        'error': response.data.get('detail', 'ERROR'),
        'message': response.data.get('detail', str(response.data)),
        'status_code': response.status_code
    }
    
    # If there are field errors, include them
    if isinstance(response.data, dict) and 'detail' not in response.data:
        custom_response_data['errors'] = response.data
    
    # Log errors based on status code
    if response.status_code >= 500:
        logger.error(f"{response.status_code} Error: {exc}", exc_info=True)
    elif response.status_code >= 400:
        logger.warning(f"{response.status_code} Client Error: {exc}")
    
    response.data = custom_response_data
    return response

