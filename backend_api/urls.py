
from django.urls import path
from backend_api import views
from rest_framework.authtoken import views as AuthViews


urlpatterns = [
    path('movies/', views.MovieList.as_view()), # Movies List, Create Route
    path('movies/<int:pk>/', views.MovieDetail.as_view()), # Movies Detail, Update, Delete Route 

    path('users/', views.UserList.as_view()),
	path('users/<int:pk>/', views.UserDetail.as_view()),

	path('api-token-auth/', AuthViews.obtain_auth_token), # Request Valid Token

]
