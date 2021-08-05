from django.db import models
from accounts.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.TextField()
    duration = models.TextField()
    genres = models.ManyToManyField(Genre)
    launch = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()
    
class Criticism(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)