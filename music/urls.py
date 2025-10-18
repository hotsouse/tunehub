from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='music_home'),
    path('tracks/', views.track_list, name='track_list'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:album_id>/', views.album_detail, name='album_detail'),
    path('tracks/<int:track_id>/favorite/', views.toggle_favorite_track, name='toggle_favorite_track'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
]


