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


class ReviewManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form["content"]) < 2:
            errors["content"] = "Review must be at least 2 characters"

        return errors

class Review(models.Model):
    postId = models.IntegerField()
    content = models.CharField(max_length=255)
    reviewer = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likedreviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    def total_likes(self):
        return self.likes.count()

