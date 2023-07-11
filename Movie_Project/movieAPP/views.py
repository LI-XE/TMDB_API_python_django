from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
import requests
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
TMDB_API_KEY = "ad10831a1d59bb10647b7f970dc3d4d8"
# Create your views here.
def home(request):
    
    data = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1")
    movies = data.json()
    print(movies)

    context = {
        "user": request.user,
        "movies": movies["results"]
    }
    return render(request, "home.html", context)



def search(request):

    # Get the query from the search box
    query = request.GET.get('q')
    print( request.GET.get('q'))

    # If the query is not empty
    if query:

        # Get the results from the API

        data = requests.get(f"https://api.themoviedb.org/3/search/tv?query={query}&api_key={TMDB_API_KEY}&language=en-US&include_adult=false")
        print(data.json()["results"])
    else:
        return HttpResponse("Please enter a search query")

    # Render the template
    return render(request, 'search.html', context={
        "data": data.json()["results"],
        "type": request.GET.get("type")
    })

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