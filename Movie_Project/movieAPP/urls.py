from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register_page),
    path('login', views.login_page),
    path('logout', views.logout_user),
    path('profile', views.profile_page),
    path('favorite', views.favorite_page),
    path('search', views.search),
    # path('profile/<int:user_id>', views.user_profile),
    # path('movies/<int:movie_id>', views.movie_detail),
    # path('movies/<int:movie_id>/add/favorite', views.add_favorite),
    # path('movies/<int:movie_id>/remove/favorite', views.remove_favorite),
    # path('comment/<int:comment_id>/delete/<int:movie_id>', views.comment_delete),
    # path('comment/<int:comment_id>/create', views.create_comment),
]
