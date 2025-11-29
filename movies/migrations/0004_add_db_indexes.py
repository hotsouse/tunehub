# Generated migration for database indexes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_review'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='movie_genre_name_idx'),
        ),
        migrations.AddIndex(
            model_name='director',
            index=models.Index(fields=['name'], name='director_name_idx'),
        ),
        migrations.AddIndex(
            model_name='actor',
            index=models.Index(fields=['name'], name='actor_name_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['title'], name='movie_title_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['release_year'], name='movie_year_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['rating'], name='movie_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['release_year', 'rating'], name='movie_year_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['movie', 'created_at'], name='review_movie_date_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['user', 'created_at'], name='review_user_date_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['rating'], name='review_rating_idx'),
        ),
    ]

