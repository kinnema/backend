from django.contrib.auth.models import User
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField()
    poster_path = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
