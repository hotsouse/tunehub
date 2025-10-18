from rest_framework import serializers
from movies.models import Movie, Genre as MovieGenre, Director, Actor, Review


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = ["id", "name"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "name", "bio"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "bio"]


class MovieSerializer(serializers.ModelSerializer):
    genres = MovieGenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MovieGenre.objects.all(), source="genres", write_only=True
    )
    directors = DirectorSerializer(many=True, read_only=True)
    director_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Director.objects.all(), source="directors", write_only=True
    )
    actors = ActorSerializer(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), source="actors", write_only=True
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "release_year",
            "duration",
            "rating",
            "genres",
            "genre_ids",
            "directors",
            "director_ids",
            "actors",
            "actor_ids",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "movie", "user", "rating", "comment", "created_at"]
        read_only_fields = ["user", "created_at"]
