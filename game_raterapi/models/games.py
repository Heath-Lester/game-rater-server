from django.db import models


class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time = models.TimeField(auto_now=False, auto_now_add=False)
    age_recommendation = models.IntegerField()