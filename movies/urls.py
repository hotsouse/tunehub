from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/favorite/', views.toggle_favorite_movie, name='toggle_favorite_movie'),
    path('add/', views.add_movie, name='add_movie'),
    path('<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
]
