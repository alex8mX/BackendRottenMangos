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

	rating_average = models.FloatField(default=0)

	def update_review_fields(self):
		reviews = self.reviews.all()
		self.rating_average = reviews.aggregate(models.Avg('star_rating')).get('star_rating__avg')
		self.save(update_fields=['rating_average'])

	def __str__(self):
		return self.title

class Review(models.Model):
	movie = models.ForeignKey(Movie, related_name = 'reviews', on_delete=models.CASCADE)
	star_rating = models.IntegerField(null=False, validators = [MaxValueValidator(5),MinValueValidator(0)])
	comment = models.CharField(max_length=250)
	owner = models.ForeignKey('auth.User', related_name = 'reviews', on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		super(Review, self).save(*args,**kwargs)
		self.movie.update_review_fields()

	def __str__(self):
		return u'User: %s. Rating: %s Stars. Review: %s.' % (self.owner.username, self.star_rating, self.comment)

class Watchlist(models.Model):
	movie = models.ForeignKey(Movie, related_name = 'watchlists', on_delete=models.CASCADE)
	owner = models.ForeignKey('auth.User', related_name = 'watchlists', on_delete=models.CASCADE)

	class Meta:
		unique_together = ["movie","owner"]