from django.db import models


class Rating(models.Model):

    gamer = models.ForeignKey("User", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.IntegerField()