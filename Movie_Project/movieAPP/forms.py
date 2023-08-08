from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

class UserEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=255, min_length=3, required=True)
    last_name = forms.CharField(max_length=255, min_length=3, required=True)
    username = forms.CharField(max_length=255, min_length=3, required=True)
    email = forms.EmailField(max_length=255, required=True, disabled=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

class UpdateProfile(forms.ModelForm):
    image = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Profile
        fields = ("image",)
