from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Director, Actor
from music.models import Album, Track, Artist, Genre as MusicGenre


class Command(BaseCommand):
    help = 'Load basic test data'

    def handle(self, *args, **options):
        # Movies
        action, _ = Genre.objects.get_or_create(name='Action')
        drama, _ = Genre.objects.get_or_create(name='Drama')
        comedy, _ = Genre.objects.get_or_create(name='Comedy')
        
        nolan, _ = Director.objects.get_or_create(name='Christopher Nolan')
        dicaprio, _ = Actor.objects.get_or_create(name='Leonardo DiCaprio')
        
        Movie.objects.get_or_create(
            title='Inception',
            defaults={
                'description': 'A thief who steals corporate secrets through dream-sharing technology.',
                'release_year': 2010,
                'duration': 148,
                'rating': 8.8
            }
        )
        
        # Music
        rock, _ = MusicGenre.objects.get_or_create(name='Rock')
        pop, _ = MusicGenre.objects.get_or_create(name='Pop')
        
        beatles, _ = Artist.objects.get_or_create(name='The Beatles')
        
        album, _ = Album.objects.get_or_create(
            title='Abbey Road',
            artist=beatles,
            defaults={'release_year': 1969}
        )
        album.genres.add(rock, pop)
        
        Track.objects.get_or_create(
            title='Come Together',
            album=album,
            defaults={'duration': 259, 'rating': 4.8}
        )
        
        self.stdout.write(self.style.SUCCESS('Test data loaded!'))
