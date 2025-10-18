from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, AlbumViewSet, PlaylistViewSet, MovieViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]


