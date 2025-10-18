from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    formed_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_year = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    # 👇 вместо genre = models.ForeignKey(...) делаем ManyToMany
    genres = models.ManyToManyField(Genre, related_name="albums", blank=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Track(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="tracks",
        null=True,       # 👈 разрешаем null
        blank=True       # 👈 разрешаем пустое в формах
    )
    duration = models.IntegerField(help_text="Duration in seconds")
    rating = models.FloatField(default=0)
    artists = models.ManyToManyField(Artist, related_name="tracks", blank=True)

    def __str__(self):
        return f"{self.title} - {self.album.title if self.album else 'No Album'}"


class Playlist(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(Track, related_name='in_playlists', blank=True)

    def __str__(self):
        return f"{self.name} ({'public' if self.is_public else 'private'})"
