from .models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	username = serializers.CharField(max_length=32,validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(min_length=8, write_only=True)
	reviews = serializers.PrimaryKeyRelatedField(many=True, queryset=Review.objects.all(), required=False)

	def create(self, validated_data):
		user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
		return user

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password','reviews']

class WatchlistSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Watchlist
		fields = '__all__'