from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    content = models.TextField(max_length=255)
    writer = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)