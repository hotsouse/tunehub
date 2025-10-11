from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Movie, Genre, Review
from .forms import ReviewForm

def movie_list(request):
    movies = Movie.objects.all()
    
    # Search
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(directors__name__icontains=query) |
            Q(actors__name__icontains=query)
        ).distinct()
    
    # Filtering
    genre_filter = request.GET.get('genre')
    if genre_filter:
        movies = movies.filter(genres__name=genre_filter)
    
    year_filter = request.GET.get('year')
    if year_filter:
        movies = movies.filter(release_year=year_filter)
    
    rating_filter = request.GET.get('min_rating')
    if rating_filter:
        movies = movies.filter(rating__gte=float(rating_filter))
    
    # Sorting
    sort_by = request.GET.get('sort', '-release_year')
    if sort_by in ['title', 'release_year', 'rating', '-title', '-release_year', '-rating']:
        movies = movies.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.all()
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'years': years,
        'search_query': query or '',
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all().select_related('user')
    
    # Check if user has favorited this movie
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = request.user.favorite_movies.filter(id=movie_id).exists()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            
            # Update movie rating
            avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']
            movie.rating = avg_rating or 0
            movie.save()
            
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'is_favorited': is_favorited,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
def toggle_favorite_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.user.favorite_movies.filter(id=movie_id).exists():
        request.user.favorite_movies.remove(movie)
        is_favorited = False
    else:
        request.user.favorite_movies.add(movie)
        is_favorited = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})
    
    return redirect('movie_detail', movie_id=movie_id)