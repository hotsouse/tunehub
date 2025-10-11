from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from movies.models import Movie, Review
from music.models import Track, Album, Playlist
from movies.serializers import MovieSerializer, ReviewSerializer
from music.serializers import TrackSerializer, AlbumSerializer, PlaylistSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'release_year', 'rating']
    search_fields = ['title', 'description', 'directors__name', 'actors__name']
    ordering_fields = ['title', 'release_year', 'rating']
    ordering = ['-release_year']
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        movie = self.get_object()
        user = request.user
        
        if user.favorite_movies.filter(id=movie.id).exists():
            user.favorite_movies.remove(movie)
            is_favorited = False
        else:
            user.favorite_movies.add(movie)
            is_favorited = True
        
        return Response({'is_favorited': is_favorited})

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['album__genre', 'artists']
    search_fields = ['title', 'album__title', 'artists__name']
    ordering_fields = ['title', 'album__title']
    ordering = ['title']
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        track = self.get_object()
        user = request.user
        
        if user.favorite_music.filter(id=track.id).exists():
            user.favorite_music.remove(track)
            is_favorited = False
        else:
            user.favorite_music.add(track)
            is_favorited = True
        
        return Response({'is_favorited': is_favorited})

class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'artist', 'release_year']
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'release_year']
    ordering = ['-release_year']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)