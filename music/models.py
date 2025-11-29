from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='genre_name_idx'),
        ]

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    formed_year = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='artist_name_idx'),
            models.Index(fields=['country'], name='artist_country_idx'),
            models.Index(fields=['formed_year'], name='artist_year_idx'),
        ]

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_year = models.IntegerField(db_index=True)
    description = models.TextField(blank=True, null=True)

    # 👇 вместо genre = models.ForeignKey(...) делаем ManyToMany
    genres = models.ManyToManyField(Genre, related_name="albums", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['title'], name='album_title_idx'),
            models.Index(fields=['release_year'], name='album_year_idx'),
            models.Index(fields=['artist', 'release_year'], name='album_artist_year_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Track(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="tracks",
        null=True,       # 👈 разрешаем null
        blank=True       # 👈 разрешаем пустое в формах
    )
    duration = models.IntegerField(help_text="Duration in seconds")
    rating = models.FloatField(default=0, db_index=True)
    artists = models.ManyToManyField(Artist, related_name="tracks", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['title'], name='track_title_idx'),
            models.Index(fields=['rating'], name='track_rating_idx'),
            models.Index(fields=['album', 'title'], name='track_album_title_idx'),
        ]

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
