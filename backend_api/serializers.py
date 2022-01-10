from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Movie
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

	class Meta:
		model = User
		fields = ['id', 'username', 'movies']