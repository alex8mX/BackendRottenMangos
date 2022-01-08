from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from .models import Movie
from .serializers import MovieSerializer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def movie_list(request):

	if request.method == 'GET':
		movies = Movie.objects.all()
		serializer = MovieSerializer(movies, many= True)
		return JsonResponse(serializer.data, safe = False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MovieSerializer(data=data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def movie_detail(request, pk):
	try:
		movie = Movie.objects.get(pk=pk)

	except Movie.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = MovieSerializer(movie)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = MovieSerializer(movie,data=data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		movie.delete()
		return HttpResponse(status=204)
		
