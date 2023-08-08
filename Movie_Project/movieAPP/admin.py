from django.contrib import admin
from django.contrib.auth.models import User
from .models import Favorite, Review, Profile

# Register your models here.
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Favorite)