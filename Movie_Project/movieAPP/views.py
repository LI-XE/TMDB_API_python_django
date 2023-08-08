from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm, UpdateProfile, UserEditForm
from .models import Favorite, Review, Profile
import requests
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from dotenv import load_dotenv
import os



def configure():
    load_dotenv()
    
DB_API_KEY = os.getenv('DB_API_KEY')



# Home page
def home(request):
    data = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={DB_API_KEY}&language=en-US&page=1")
    movies = data.json()
    print(movies)
    print(request.user)
    context = {
        "current_user": request.user,
        "movies": movies["results"],
    }
    return render(request, "home.html", context)

def loadmoreJson(request, current_page):
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
        return render(request, 'search.html', context={
        "data": data.json()["results"], "current_user": request.user
        })
    else:
        return HttpResponse("Please enter a search query")
        
    # Render the template
    


# Get Movie Detail 
def movie_detail_page(request, movie_id):
    
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={DB_API_KEY}&language=en-US")
    if data:
        movie = data.json()
        favorites = Favorite.objects.filter(movieId = movie['id'])
        is_added_to_favorites = False
        
        if favorites:
            for favorite in favorites:
                if request.user in favorite.addTo.all():
                    is_added_to_favorites = True
        print(is_added_to_favorites)
        reviews = Review.objects.filter(postId = movie_id),
        context={
            "current_user": request.user,
            "movie": movie,
            "favorites": favorites,
            "is_added_to_favorites": is_added_to_favorites,
            "reviews": reviews[0].order_by("-created_at")
        }
        return render(request, "movieDetail.html", context)
    else:
        return HttpResponse("Sorry! This movie doesn't have movie detail.")
    

#  Post Review
@login_required
def post_reviews(request, movie_id):
    if request.POST:
        errors = Review.objects.validate(request.POST)
        if errors:
            for e in errors:
                messages.error(request, e)
            return redirect(f"/movies/{movie_id}")
        
        review = Review.objects.create(postId=int(movie_id), content=request.POST["content"], reviewer=request.user )
        print(review)
        return redirect(f"/movies/{movie_id}")


#  Like or dislike Review
@login_required
def likes_review(request, movie_id, review_id):
    review = Review.objects.get(id= review_id)
    liked_review = False
    if review.likes.filter(id=request.user.id).exists():
        review.likes.remove(request.user)
        liked_review = False
    else:   
        review.likes.add(request.user)
        liked_review = True
    return HttpResponseRedirect(f"/movies/{movie_id}")


# Delete Review
@login_required
def delete_review(request, movie_id, review_id):
    review = Review.objects.get(id = review_id)
    if request.user.id == review.reviewer_id:
        review.delete()
    return redirect(f"/movies/{movie_id}")



# Favorite Page
@login_required
def favorite_page(request):
    user = request.user
    context = {
        "current_user": request.user,
        "favorites": user.favorites.all()
    }
    print(user.favorites.all())
    
    return render(request, "favorite.html", context)


# Add to my favorites
@login_required
def add_to_favorite(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={DB_API_KEY}&language=en-US")
    if data:
        favorite_movie = data.json()
        favorite = Favorite.objects.create(movieId =int(favorite_movie['id']), movieTitle = favorite_movie['original_title'], moviePost = favorite_movie['poster_path'])
        if favorite not in request.user.favorites.all():
            favorite.addTo.add(request.user)
    return redirect(f"/movies/{movie_id}")


# Remove from my favorites
@login_required
def remove_from_favorite(request, movie_id):
    movies = Favorite.objects.filter(movieId=movie_id)
    if movies:
        for movie in movies:
            if request.user in movie.addTo.all():
                movie.addTo.remove(request.user)
    return redirect(f"/movies/{movie_id}")



# Profile Page
def user_profile_page(request, user_id):
    user = User.objects.get(id=user_id)
    current_user = User.objects.get(id= request.user.id)
    profile_user = Profile.objects.get(user__id = request.user.id)

    user_form = UserEditForm( instance=current_user)
    profile_form = UpdateProfile(instance=profile_user)
    
    context={
        "current_user" : current_user,
        "user": user,
        "user_form": user_form,
        "profile_form": profile_form
    }
    return render(request, "profile.html", context)

# update profile photo
@login_required
def update_profile_photo(request, user_id):
    current_user = User.objects.get(id= request.user.id)
    profile_user = Profile.objects.get(user__id = user_id)
     
    if request.method == "POST":
        profile_form = UpdateProfile(request.POST, request.FILES, instance=profile_user)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your Profile Photo has been updated successfully.")
            return redirect(f"/profile/{user_id}")
        else:
            context={
                "current_user" : current_user,
                "user": User.objects.get(id=user_id),
                "profile_form": profile_form
            }
            return render(request, "profile.html", context)
        
# update profile info
@login_required
def update_user_profile(request, user_id):
    current_user = User.objects.get(id= request.user.id)
     
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            updated_user = user_form.save()
            # login(request, updated_user)
            messages.success(request, "Your Profile has been updated successfully.")
            return redirect(f"/profile/{user_id}")
        else:
            context={
                "current_user" : current_user,
                "user": User.objects.get(id=user_id),
                "user_form": user_form,
            }
            return render(request, "profile.html", context)

    # context={
    #     "current_user" : current_user,
    #     "user": User.objects.get(id=user_id),
    #     "user_form": user_form,
    #     "profile_form": profile_form
    # }
    # return render(request, "profile.html", context)


def register_page(request):

    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)

        if reg_form.is_valid():
            new_user = reg_form.save()
            login(request, new_user)
            Profile.objects.create(user = new_user, image="noAvatar.png")
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



