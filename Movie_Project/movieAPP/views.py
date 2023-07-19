from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
from .models import Favorite
import requests
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from dotenv import load_dotenv
import os



def configure():
    load_dotenv()
    
DB_API_KEY = os.getenv('DB_API_KEY')



# Home page
def home(request):
    configure()
    data = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={DB_API_KEY}&language=en-US&page=1")
    movies = data.json()

    context = {
        "user": request.user,
        "movies": movies["results"],
    }
    return render(request, "home.html", context)

def loadmoreJson(request, current_page):
    # currentPage += 1
    data = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={DB_API_KEY}&language=en-US&page={current_page}")
    return JsonResponse({'data': data.json(), 'current_page':current_page})


# Search Movies
def search(request):

    # Get the query from the search box
    query = request.GET.get('q')
    print( request.GET.get('q'))

    # If the query is not empty
    if query:

        # Get the results from the API

        data = requests.get(f"https://api.themoviedb.org/3/search/tv?query={query}&api_key={DB_API_KEY}&language=en-US&include_adult=false")
        print(data.json()["results"])
    else:
        return HttpResponse("Please enter a search query")

    # Render the template
    return render(request, 'search.html', context={
        "data": data.json()["results"],
    })


# Get Movie Detail 
def movie_detail_page(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={DB_API_KEY}&language=en-US")
    if data:
        movie = data.json()
        print(data)
        context={
            "movie": movie,
        }
    else:
        return HttpResponse("Sorry! This movie doesn't have movie detail.")
    return render(request, "movieDetail.html", context)




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


def favorite_page(request):
    return render(request, "favorite.html")