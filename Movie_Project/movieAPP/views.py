from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    context = {
        "user": request.user
    }
    return render(request, "home.html", context)

def register_page(request):

    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)

        if reg_form.is_valid():
            new_user = reg_form.save()
            login(request, new_user)
            print(new_user)
            return redirect("/")
        else:
            context = {"reg_form": reg_form}
            return render(request, "register.html", context)
    else:
        return render(request, "register.html", context={"user": None, "reg_form": RegistrationForm()})


def login_page(request):
    if request.method == "POST":
        log_form = AuthenticationForm(data=request.POST)
        if log_form.is_valid():
            user = log_form.get_user()
            login(request, user)
            return redirect("/")
        else:
            context = {"log_form": log_form}
            print(context)
            return render(request, "login.html", context)

    else:
        return render(request, "login.html", context={"log_form": AuthenticationForm()})


def logout_user(request):
    logout(request)
    return redirect("/")

def profile_page(request):
    return render(request, "profile.html")

def movie_detail(request):
    return render(request, "movieDetail.html")

def favorite_page(request):
    return render(request, "favorite.html")