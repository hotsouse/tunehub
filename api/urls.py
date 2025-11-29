from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, AlbumViewSet, PlaylistViewSet, MovieViewSet, ReviewViewSet
from .auth_views import api_register, api_login, api_logout, api_user_info
from .health_views import health_check, health_detailed, health_ready, health_live

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/register/', api_register, name='api-register'),
    path('auth/login/', api_login, name='api-login'),
    path('auth/logout/', api_logout, name='api-logout'),
    path('auth/user/', api_user_info, name='api-user-info'),
    # Health check endpoints
    path('health/', health_check, name='api-health'),
    path('health/detailed/', health_detailed, name='api-health-detailed'),
    path('health/ready/', health_ready, name='api-health-ready'),
    path('health/live/', health_live, name='api-health-live'),
]


