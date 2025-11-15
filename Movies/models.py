from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    poster_url = models.URLField(blank=True, null=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)   # changed to DateField
    tmdb_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=0)  # changed to PositiveSmallIntegerField
    comment = models.TextField(blank=True)                # allowed blank comment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.movie.title} ({self.rating})"
