from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='movie_genre_name_idx'),
        ]

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='director_name_idx'),
        ]

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='actor_name_idx'),
        ]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    release_year = models.IntegerField(db_index=True)
    duration = models.IntegerField(
        default=90,  # <-- добавлен дефолт (например, 90 минут)
        help_text="Duration in minutes"
    )
    rating = models.FloatField(default=0, db_index=True)

    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    directors = models.ManyToManyField(Director, related_name="movies", blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['title'], name='movie_title_idx'),
            models.Index(fields=['release_year'], name='movie_year_idx'),
            models.Index(fields=['rating'], name='movie_rating_idx'),
            models.Index(fields=['release_year', 'rating'], name='movie_year_rating_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="movie_reviews")
    rating = models.IntegerField(db_index=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['movie', 'created_at'], name='review_movie_date_idx'),
            models.Index(fields=['user', 'created_at'], name='review_user_date_idx'),
            models.Index(fields=['rating'], name='review_rating_idx'),
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating})"
