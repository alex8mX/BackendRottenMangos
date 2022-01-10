from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):

	class Meta:
		model = Movie
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Review
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	reviews = serializers.PrimaryKeyRelatedField(many=True, queryset=Review.objects.all())

	class Meta:
		model = User
		fields = ['id', 'username', 'reviews']