from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

GENRES_CHOICES = (("Action","Action"),("Comedy","Comedy"),("Drama","Drama"), ("Horror","Horror"),("Romance","Romance"),("Thriller","Thriller"),)

# Create your models here.
class Movie(models.Model):
	title = models.CharField(max_length=250)
	release_date = models.DateField()
	genre = models.CharField(max_length=250, choices=GENRES_CHOICES)
	plot = models.CharField(max_length=250)


	def __str__(self):
		return self.title

class Review(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	star_rating = models.IntegerField(null=False, validators = [MaxValueValidator(5),MinValueValidator(0)])
	comment = models.CharField(max_length=250)
	owner = models.ForeignKey('auth.User', related_name = 'reviews', on_delete=models.CASCADE)

	def __str__(self):
		return u'%s stars ' % (self.star_rating)