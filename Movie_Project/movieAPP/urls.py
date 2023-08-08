from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register_page),
    path('login', views.login_page),
    path('logout', views.logout_user),
    path('favorite', views.favorite_page),
    path('search', views.search),
    path('movies/<int:movie_id>', views.movie_detail_page),
    path('loadmorejson/<int:current_page>', views.loadmoreJson),
    path('addToFavorite/<int:movie_id>', views.add_to_favorite),
    path('removeFromFavorite/<int:movie_id>', views.remove_from_favorite),
    path('movies/<int:movie_id>/add/review', views.post_reviews),
    path('movies/<int:movie_id>/likes/<int:review_id>', views.likes_review),
    path('movies/<int:movie_id>/delete/<int:review_id>', views.delete_review),
    path('profile/<int:user_id>', views.user_profile_page),
    path('update/profile/<int:user_id>', views.update_user_profile),
]
