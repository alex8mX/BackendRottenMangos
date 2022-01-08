from .models import *
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'
