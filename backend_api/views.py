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
		serializer = MovieSerializer(movies, many= True)
		return Response(serializer.data)

	def post(self,request,format=None):
		serializer = MovieSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_object(self,pk):
		try:
			return Movie.objects.get(pk=pk)

		except Movie.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def get(self, request, pk, format=None):
		movie = self.get_object(pk)
		serializer = MovieSerializer(movie)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		movie = self.get_object(pk)
		serializer = MovieSerializer(movie,data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		movie = self.get_object(pk)
		movie.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self,request, format=None):
		reviews = Review.objects.all()
		serializer = ReviewSerializer(reviews, many= True)
		return Response(serializer.data)

	def post(self,request,format=None):
		serializer = ReviewSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save(owner=self.request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

	def get_object(self,pk):
		try:
			return Review.objects.get(pk=pk)

		except Review.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def get(self, request, pk, format=None):
		review = self.get_object(pk)
		serializer = ReviewSerializer(review)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		review = self.get_object(pk)
		serializer = ReviewSerializer(review,data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		review = self.get_object(pk)
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
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)