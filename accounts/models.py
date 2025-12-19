from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    favorite_movies = models.ManyToManyField("movies.Movie", related_name="favored_by_users", blank=True)
    favorite_music = models.ManyToManyField("music.Track", related_name="favored_by_users", blank=True)
