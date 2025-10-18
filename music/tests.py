from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from .models import Artist, Genre, Album, Track
from movies.models import Movie, Genre as MovieGenre, Director, Actor


class MusicApiTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="u1", password="pass12345")
        self.artist = Artist.objects.create(name="Artist A")
        self.genre = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(title="Album A", artist=self.artist, release_year=2020)
        self.album.genres.add(self.genre)
        self.track = Track.objects.create(title="Track A", album=self.album, duration=180)
        self.track.artists.add(self.artist)

    def test_list_tracks(self):
        resp = self.client.get("/api/tracks/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)

    def test_filter_tracks_by_genre(self):
        resp = self.client.get("/api/tracks/", {"album__genres": self.genre.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)

    def test_create_playlist_requires_auth(self):
        resp = self.client.post("/api/playlists/", {"name": "MyP", "description": "d", "track_ids": [self.track.id]})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username="u1", password="pass12345")
        resp2 = self.client.post("/api/playlists/", {"name": "MyP", "description": "d", "track_ids": [self.track.id]})
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)


class MoviesApiTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="u2", password="pass12345")
        self.mgenre = MovieGenre.objects.create(name="Drama")
        self.dir = Director.objects.create(name="Nolan")
        self.actor = Actor.objects.create(name="DiCaprio")
        self.movie = Movie.objects.create(title="Inception", description="dreams", release_year=2010, duration=148)
        self.movie.genres.add(self.mgenre)
        self.movie.directors.add(self.dir)
        self.movie.actors.add(self.actor)

    def test_list_movies(self):
        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)

    def test_search_and_filter_movies(self):
        resp = self.client.get("/api/movies/", {"search": "dreams", "genres__name": "Drama"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)

    def test_ordering_movies(self):
        resp = self.client.get("/api/movies/", {"ordering": "-release_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_toggle_favorite_requires_auth(self):
        url = f"/api/movies/{self.movie.id}/toggle_favorite/"
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username="u2", password="pass12345")
        resp2 = self.client.post(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)


