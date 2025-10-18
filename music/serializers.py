from rest_framework import serializers
from .models import Genre, Artist, Album, Track, Playlist


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name", "bio", "country", "formed_year"]


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source="artist", write_only=True
    )
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), source="genres", write_only=True
    )

    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "artist",
            "artist_id",
            "release_year",
            "description",
            "genres",
            "genre_ids",
        ]


class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    album_id = serializers.PrimaryKeyRelatedField(
        allow_null=True, required=False, queryset=Album.objects.all(), source="album", write_only=True
    )
    artists = ArtistSerializer(many=True, read_only=True)
    artist_ids = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Artist.objects.all(), source="artists", write_only=True
    )

    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "duration",
            "rating",
            "album",
            "album_id",
            "artists",
            "artist_ids",
        ]


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    track_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Track.objects.all(), source="tracks", write_only=True
    )

    class Meta:
        model = Playlist
        fields = ["id", "name", "description", "is_public", "tracks", "track_ids"]

