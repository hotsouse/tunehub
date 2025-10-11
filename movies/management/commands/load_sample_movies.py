
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Director, Actor

class Command(BaseCommand):
    help = 'Load sample movie data'

    def handle(self, *args, **options):
        # Создаем жанры
        action, created = Genre.objects.get_or_create(name='Action')
        drama, created = Genre.objects.get_or_create(name='Drama')
        comedy, created = Genre.objects.get_or_create(name='Comedy')
        scifi, created = Genre.objects.get_or_create(name='Sci-Fi')
        romance, created = Genre.objects.get_or_create(name='Romance')
        
        self.stdout.write('Created genres...')

        # Создаем режиссеров
        nolan, created = Director.objects.get_or_create(
            name='Christopher Nolan',
            bio='British-American film director known for Inception, The Dark Knight.'
        )
        spielberg, created = Director.objects.get_or_create(
            name='Steven Spielberg', 
            bio='American film director known for Jurassic Park, Saving Private Ryan.'
        )
        cameron, created = Director.objects.get_or_create(
            name='James Cameron',
            bio='Canadian film director known for Titanic, Avatar.'
        )
        
        self.stdout.write('Created directors...')

        # Создаем актеров
        dicaprio, created = Actor.objects.get_or_create(
            name='Leonardo DiCaprio',
            bio='American actor and film producer.'
        )
        bale, created = Actor.objects.get_or_create(
            name='Christian Bale',
            bio='British actor known for his roles in American Psycho and The Dark Knight.'
        )
        winslet, created = Actor.objects.get_or_create(
            name='Kate Winslet',
            bio='British actress known for Titanic and The Reader.'
        )
        
        self.stdout.write('Created actors...')

        # Создаем фильмы
        movies_data = [
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_year': 2010,
                'duration': 148,
                'genres': [action, scifi],
                'directors': [nolan],
                'actors': [dicaprio],
                'rating': 8.8
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_year': 2008,
                'duration': 152,
                'genres': [action, drama],
                'directors': [nolan],
                'actors': [bale],
                'rating': 9.0
            },
            {
                'title': 'Titanic',
                'description': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
                'release_year': 1997,
                'duration': 195,
                'genres': [drama, romance],
                'directors': [cameron],
                'actors': [dicaprio, winslet],
                'rating': 7.9
            },
            {
                'title': 'Jurassic Park',
                'description': 'A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park\'s cloned dinosaurs to run loose.',
                'release_year': 1993,
                'duration': 127,
                'genres': [action, scifi],
                'directors': [spielberg],
                'actors': [],
                'rating': 8.2
            },
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'release_year': 1994,
                'duration': 142,
                'genres': [drama],
                'directors': [],
                'actors': [],
                'rating': 9.3
            }
        ]
        
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['description'],
                    'release_year': movie_data['release_year'],
                    'duration': movie_data['duration'],
                    'rating': movie_data['rating']
                }
            )
            if created:
                if movie_data['genres']:
                    movie.genres.set(movie_data['genres'])
                if movie_data['directors']:
                    movie.directors.set(movie_data['directors'])
                if movie_data['actors']:
                    movie.actors.set(movie_data['actors'])
                self.stdout.write(f'Created movie: {movie.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample movies!')
        )
