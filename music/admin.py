from django.contrib import admin
from .models import Genre, Artist, Album, Track, Playlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "formed_year")
    search_fields = ("name", "country")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_year")
    list_filter = ("release_year", "genres")
    search_fields = ("title", "artist__name")


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "duration", "rating")
    list_filter = ("album", "artists")
    search_fields = ("title", "album__title", "artists__name")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_public")
    search_fields = ("name", "user__username")


