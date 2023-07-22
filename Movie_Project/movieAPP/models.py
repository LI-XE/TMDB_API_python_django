from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Favorite(models.Model):
    movieId = models.IntegerField()
    movieTitle = models.CharField(max_length=255)
    moviePost = models.ImageField(blank=True)
    addTo = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.movieTitle


