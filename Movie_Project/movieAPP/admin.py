from django.contrib import admin
from django.contrib.auth.models import User
from .models import Favorite

# Register your models here.
# admin.site.register(User)
# admin.site.register(Comment)
admin.site.register(Favorite)