from django.contrib import admin
from django.contrib.auth.models import User
from .models import Favorite, Review

# Register your models here.
admin.site.register(Review)
# admin.site.register(Comment)
admin.site.register(Favorite)