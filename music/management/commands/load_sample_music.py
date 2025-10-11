from django.core.management.base import BaseCommand
from music.models import Genre, Artist, Album, Track


class Command(BaseCommand):
    help = "Load sample music data"

    def handle(self, *args, **kwargs):
        # Создаём жанры
        rock, _ = Genre.objects.get_or_create(name="Rock")
        pop, _ = Genre.objects.get_or_create(name="Pop")

        self.stdout.write(self.style.SUCCESS("Created music genres..."))

        # Создаём артистов (ищем только по name, остальные данные в defaults)
        beatles, _ = Artist.objects.get_or_create(
            name="The Beatles",
            defaults={
                "bio": "Legendary English rock band formed in Liverpool.",
                "country": "UK",
                "formed_year": 1960,
            },
        )

        self.stdout.write(self.style.SUCCESS("Created artists..."))

        # Создаём альбом (ищем по title + artist, остальные данные в defaults)
        abbey_road, created = Album.objects.get_or_create(
            title="Abbey Road",
            artist=beatles,
            defaults={
                "release_year": 1969,
                "description": "The eleventh studio album by the English rock band the Beatles.",
            },
        )

        # 👇 Привязываем жанры (правильно через set/add, а не в get_or_create)
        abbey_road.genres.add(rock, pop)

        if created:
            self.stdout.write(self.style.SUCCESS("Created album Abbey Road"))
        else:
            self.stdout.write(self.style.WARNING("Album Abbey Road already exists"))

        # Создаём треки (ищем по title + album, остальное в defaults)
        Track.objects.get_or_create(
            title="Come Together",
            album=abbey_road,
            defaults={
                "duration": 259,
                "rating": 4.8,
            },
        )

        Track.objects.get_or_create(
            title="Something",
            album=abbey_road,
            defaults={
                "duration": 183,
                "rating": 4.7,
            },
        )

        self.stdout.write(self.style.SUCCESS("Created tracks for Abbey Road"))
