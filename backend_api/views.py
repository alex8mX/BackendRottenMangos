from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.contrib.auth.models import User


# Create your views here.
class MovieList(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self,request, format=None):
		movies = Movie.objects.all()
		if movies:
			serializer = MovieSerializer(movies, many= True)
			return Response(serializer.data)
		else:
			return Response({"message":"No movies registered!"}, status = status.HTTP_404_NOT_FOUND)

	def post(self,request,format=None):
		serializer = MovieSerializer(data=request.data)

		if serializer.is_valid():
			movie = serializer.save()
			if movie:
				return Response({"message":"Movie created successfully!", "data":serializer.data}, status=status.HTTP_201_CREATED)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_object(self,pk):
		try:
			return Movie.objects.get(pk=pk)

		except Movie.DoesNotExist:
			return Response({"message":"There is no Movie with that id!"},status=status.HTTP_404_NOT_FOUND)

	def get(self, request, pk, format=None):
		movie = self.get_object(pk)
		serializer = MovieSerializer(movie)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		movie = self.get_object(pk)
		serializer = MovieSerializer(movie,data=request.data)

		if serializer.is_valid():
			movie = serializer.save()
			if movie:
				return Response({"message":"Movie updated successfully!", "data":serializer.data}, status=status.HTTP_200_OK)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		movie = self.get_object(pk)
		movie.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self,request, format=None):
		reviews = Review.objects.all()
		if reviews:
			serializer = ReviewSerializer(reviews, many= True)
			return Response(serializer.data)
		else:
			return Response({"message":"No reviews registered!"}, status = status.HTTP_404_NOT_FOUND)

	def post(self,request,format=None):
		serializer = ReviewSerializer(data=request.data)

		if serializer.is_valid():
			review = serializer.save(owner=self.request.user)
			if review:
				return Response({"message":"Review created successfully!", "data":serializer.data}, status=status.HTTP_201_CREATED)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

	def get_object(self,pk):
		try:
			return Review.objects.get(pk=pk)

		except Review.DoesNotExist:
			return Response({"message":"There is no Review with that id!"},status=status.HTTP_404_NOT_FOUND)

	def get(self, request, pk, format=None):
		review = self.get_object(pk)
		serializer = ReviewSerializer(review)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		review = self.get_object(pk)

		if self.request.user != review.owner:
			return Response({"Error":"This is not your review, you can't change it!"},status=status.HTTP_403_FORBIDDEN)

		serializer = ReviewSerializer(review,data=request.data)

		if serializer.is_valid():
			review = serializer.save()
			if review:
				return Response({"message":"Review updated successfully!", "data":serializer.data}, status=status.HTTP_200_OK)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)	

	def delete(self, request, pk, format=None):
		review = self.get_object(pk)

		if self.request.user != review.owner:
			return Response({"Error":"This is not your review! you can't delete it!"},status=status.HTTP_403_FORBIDDEN)
		review.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserCreate(APIView):

	def post(self,request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user=user)
				json = serializer.data
				json['token'] = token.key
				return Response(json, status=status.HTTP_201_CREATED)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)	


class WatchlistList(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self,request, format=None):
		watchlists = Watchlist.objects.all()

		if watchlists:
			serializer = WatchlistSerializer(watchlists, many= True)
			return Response(serializer.data)
		else:
			return Response({"message":"No watchlists registered!"}, status = status.HTTP_404_NOT_FOUND)

	def post(self,request,format=None):
		serializer = WatchlistSerializer(data=request.data)

		if serializer.is_valid():
			watchlist = serializer.save(owner=self.request.user)
			if watchlist:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response({"message": "An error has ocurred! Check with the administrator"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({"message":"An error has ocurred with the request, please check again!", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)	

class WatchlistDetail(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_object(self,pk):
		try:
			return Watchlist.objects.get(pk=pk)

		except Watchlist.DoesNotExist:
			return Response({"message":"There is no Watchlist with that id!"},status=status.HTTP_404_NOT_FOUND)

	def get(self, request, pk, format=None):
		watchlist = self.get_object(pk)

		if self.request.user != watchlist.owner:
			return Response({"Error":"This is not your watchlist!"},status=status.HTTP_403_FORBIDDEN)

		serializer = WatchlistSerializer(watchlist)
		return Response(serializer.data)

	def delete(self, request, pk, format=None):
		watchlist = self.get_object(pk)

		if self.request.user != watchlist.owner:
			return Response({"Error":"This is not your watchlist! you can't delete it!"},status=status.HTTP_403_FORBIDDEN)

		watchlist.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)