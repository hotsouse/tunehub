# Generated migration for database indexes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_track_artists_playlist'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genre_name_idx'),
        ),
        migrations.AddIndex(
            model_name='artist',
            index=models.Index(fields=['name'], name='artist_name_idx'),
        ),
        migrations.AddIndex(
            model_name='artist',
            index=models.Index(fields=['country'], name='artist_country_idx'),
        ),
        migrations.AddIndex(
            model_name='artist',
            index=models.Index(fields=['formed_year'], name='artist_year_idx'),
        ),
        migrations.AddIndex(
            model_name='album',
            index=models.Index(fields=['title'], name='album_title_idx'),
        ),
        migrations.AddIndex(
            model_name='album',
            index=models.Index(fields=['release_year'], name='album_year_idx'),
        ),
        migrations.AddIndex(
            model_name='album',
            index=models.Index(fields=['artist', 'release_year'], name='album_artist_year_idx'),
        ),
        migrations.AddIndex(
            model_name='track',
            index=models.Index(fields=['title'], name='track_title_idx'),
        ),
        migrations.AddIndex(
            model_name='track',
            index=models.Index(fields=['rating'], name='track_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='track',
            index=models.Index(fields=['album', 'title'], name='track_album_title_idx'),
        ),
    ]

