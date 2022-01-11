
from django.urls import path
from backend_api import views
from rest_framework.authtoken import views as AuthViews


urlpatterns = [
    path('movies/', views.MovieList.as_view()), # Movies List, Create Route
    path('movies/<int:pk>/', views.MovieDetail.as_view()), # Movies Detail, Update, Delete Route

    path('reviews/', views.ReviewList.as_view()), # Reviews List, Create Route
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()), # Reviews Detail, Update, Delete Route

    path('watchlist/', views.WatchlistList.as_view()),
    path('watchlist/<int:pk>/',views.WatchlistDetail.as_view()),

    path('users/', views.UserList.as_view()), # User List
	path('users/<int:pk>/', views.UserDetail.as_view()), # User Detail

	path('users/create', views.UserCreate.as_view(), name='user-create'), # Create User Route

	path('api-token-auth/', AuthViews.obtain_auth_token), # Request Valid Token

]
