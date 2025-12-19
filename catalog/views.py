from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from music.models import Track, Album
from movies.models import Movie
from movies.forms import MovieForm
from music.forms import TrackForm, AlbumForm

def home(request):
    # Get popular tracks (sorted by rating, limit to 10)
    popular_tracks = Track.objects.select_related('album', 'album__artist').prefetch_related('artists').order_by('-rating', 'title')[:10]
    
    context = {
        'popular_tracks': popular_tracks,
    }
    return render(request, 'home.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    """Кастомная админ-панель для управления фильмами и музыкой"""
    movies = Movie.objects.all().order_by('-release_year', 'title')
    tracks = Track.objects.all().select_related('album', 'album__artist').prefetch_related('artists').order_by('title')
    albums = Album.objects.all().select_related('artist').order_by('-release_year', 'title')
    
    # Handle form submissions
    movie_form = MovieForm()
    track_form = TrackForm()
    album_form = AlbumForm()
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'movie':
            movie_form = MovieForm(request.POST)
            if movie_form.is_valid():
                movie = movie_form.save()
                messages.success(request, f'Фильм "{movie.title}" успешно добавлен!')
                return redirect('admin_panel')
        elif form_type == 'track':
            track_form = TrackForm(request.POST)
            if track_form.is_valid():
                track = track_form.save()
                messages.success(request, f'Трек "{track.title}" успешно добавлен!')
                return redirect('admin_panel')
        elif form_type == 'album':
            album_form = AlbumForm(request.POST)
            if album_form.is_valid():
                album = album_form.save()
                messages.success(request, f'Альбом "{album.title}" успешно добавлен!')
                return redirect('admin_panel')
    
    context = {
        'movies': movies,
        'tracks': tracks,
        'albums': albums,
        'movie_form': movie_form,
        'track_form': track_form,
        'album_form': album_form,
    }
    return render(request, 'admin.html', context)


