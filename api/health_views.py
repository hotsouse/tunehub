"""
Health check endpoints for monitoring
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Basic health check endpoint
    GET /api/health/
    """
    return Response({
        'status': 'healthy',
        'service': 'Movie Music Catalog API'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_detailed(request):
    """
    Detailed health check with database and cache status
    GET /api/health/detailed/
    """
    health_status = {
        'status': 'healthy',
        'service': 'Movie Music Catalog API',
        'checks': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['checks']['database'] = 'error'
        health_status['status'] = 'unhealthy'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = 'ok'
        else:
            health_status['checks']['cache'] = 'error'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status['checks']['cache'] = 'error'
        health_status['status'] = 'unhealthy'
    
    http_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_status, status=http_status)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_ready(request):
    """
    Readiness probe - checks if service is ready to accept traffic
    GET /api/health/ready/
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({
            'status': 'ready',
            'service': 'Movie Music Catalog API'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return Response({
            'status': 'not ready',
            'service': 'Movie Music Catalog API',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_live(request):
    """
    Liveness probe - checks if service is alive
    GET /api/health/live/
    """
    return Response({
        'status': 'alive',
        'service': 'Movie Music Catalog API'
    }, status=status.HTTP_200_OK)

