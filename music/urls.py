from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.album_list, name='music_home'),
    path('tracks/', views.track_list, name='track_list'),
    path('tracks/<int:track_id>/', views.track_detail, name='track_detail'),
    path('tracks/add/', views.add_track, name='add_track'),
    path('tracks/<int:track_id>/edit/', views.edit_track, name='edit_track'),
    path('tracks/<int:track_id>/delete/', views.delete_track, name='delete_track'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:album_id>/', views.album_detail, name='album_detail'),
    path('albums/add/', views.add_album, name='add_album'),
    path('albums/<int:album_id>/edit/', views.edit_album, name='edit_album'),
    path('albums/<int:album_id>/delete/', views.delete_album, name='delete_album'),
    path('tracks/<int:track_id>/favorite/', views.toggle_favorite_track, name='toggle_favorite_track'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
]


