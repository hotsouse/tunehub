from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Track, Album, Artist, Genre, Playlist
from .forms import PlaylistForm, TrackForm, AlbumForm

def track_list(request):
    tracks = Track.objects.all().select_related('album', 'album__artist')
    
    # Handle form submission for adding tracks (admin only)
    track_form = TrackForm()
    if request.method == 'POST' and request.user.is_staff:
        form_type = request.POST.get('form_type')
        if form_type == 'add_track':
            track_form = TrackForm(request.POST)
            if track_form.is_valid():
                track = track_form.save()
                messages.success(request, f'Трек "{track.title}" успешно добавлен!')
                return redirect('music:track_list')
    
    # Search
    query = request.GET.get('search') or request.GET.get('q')
    if query:
        tracks = tracks.filter(
            Q(title__icontains=query) |
            Q(album__title__icontains=query) |
            Q(artists__name__icontains=query)
        ).distinct()
    
    # Filtering
    genre_filter = request.GET.get('genre')
    if genre_filter:
        tracks = tracks.filter(album__genres__id=genre_filter)
    
    artist_filter = request.GET.get('artist')
    if artist_filter:
        tracks = tracks.filter(artists__name=artist_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', 'title')
    if sort_by in ['title', 'album__title', '-title', '-album__title', 'duration', '-duration', 'rating', '-rating', 'id', '-id']:
        tracks = tracks.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(tracks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.all()
    artists = Artist.objects.all()
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'artists': artists,
        'search_query': query or '',
        'track_form': track_form,
    }
    return render(request, 'music/track_list.html', context)

def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = request.user.favorite_music.filter(id=track_id).exists()
    
    context = {
        'track': track,
        'is_favorited': is_favorited,
    }
    return render(request, 'music/track_detail.html', context)

def album_list(request):
    albums = Album.objects.all().select_related('artist').prefetch_related('genres')
    
    # Handle form submission for adding albums (admin only)
    album_form = AlbumForm()
    if request.method == 'POST' and request.user.is_staff:
        form_type = request.POST.get('form_type')
        if form_type == 'add_album':
            album_form = AlbumForm(request.POST)
            if album_form.is_valid():
                album = album_form.save()
                messages.success(request, f'Альбом "{album.title}" успешно добавлен!')
                return redirect('music:album_list')
    
    query = request.GET.get('q')
    if query:
        albums = albums.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        )
    
    genre_filter = request.GET.get('genre')
    if genre_filter:
        albums = albums.filter(genres__name=genre_filter)
    
    paginator = Paginator(albums, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.all()
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'search_query': query or '',
        'album_form': album_form,
    }
    return render(request, 'music/album_list.html', context)

def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    tracks = album.tracks.all().select_related('album')
    
    context = {
        'album': album,
        'tracks': tracks,
    }
    return render(request, 'music/album_detail.html', context)

@login_required
def toggle_favorite_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    
    if request.user.favorite_music.filter(id=track_id).exists():
        request.user.favorite_music.remove(track)
        is_favorited = False
    else:
        request.user.favorite_music.add(track)
        is_favorited = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})
    
    return redirect('music:track_list')

@login_required
def playlist_list(request):
    playlists = request.user.playlists.all()
    
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('music:playlist_list')
    else:
        form = PlaylistForm()
    
    context = {
        'playlists': playlists,
        'form': form,
    }
    return render(request, 'music/playlist_list.html', context)

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        if track_id:
            track = get_object_or_404(Track, id=track_id)
            if track in playlist.tracks.all():
                playlist.tracks.remove(track)
            else:
                playlist.tracks.add(track)
    
    context = {
        'playlist': playlist,
    }
    return render(request, 'music/playlist_detail.html', context)


# Admin views for music management
@user_passes_test(lambda u: u.is_staff)
def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save()
            messages.success(request, f'Трек "{track.title}" успешно добавлен!')
            return redirect('admin_panel')
    else:
        form = TrackForm()
    
    return render(request, 'music/add_track.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def edit_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    if request.method == 'POST':
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, f'Трек "{track.title}" обновлен!')
            return redirect('admin_panel')
    else:
        form = TrackForm(instance=track)
    
    return render(request, 'music/edit_track.html', {'form': form, 'track': track})


@user_passes_test(lambda u: u.is_staff)
def delete_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    if request.method == 'POST':
        title = track.title
        track.delete()
        messages.success(request, f'Трек "{title}" удален!')
        return redirect('admin_panel')
    
    return render(request, 'music/delete_track.html', {'track': track})


@user_passes_test(lambda u: u.is_staff)
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save()
            messages.success(request, f'Альбом "{album.title}" успешно добавлен!')
            return redirect('admin_panel')
    else:
        form = AlbumForm()
    
    return render(request, 'music/add_album.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, f'Альбом "{album.title}" обновлен!')
            return redirect('admin_panel')
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'music/edit_album.html', {'form': form, 'album': album})


@user_passes_test(lambda u: u.is_staff)
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        title = album.title
        album.delete()
        messages.success(request, f'Альбом "{title}" удален!')
        return redirect('admin_panel')
    
    return render(request, 'music/delete_album.html', {'album': album})