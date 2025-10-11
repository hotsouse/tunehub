from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    release_year = models.IntegerField()
    duration = models.IntegerField(
        default=90,  # <-- добавлен дефолт (например, 90 минут)
        help_text="Duration in minutes"
    )
    rating = models.FloatField(default=0)

    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    directors = models.ManyToManyField(Director, related_name="movies", blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"
