from django.db import models


class Review(models.Model):

    rater = models.ForeignKey("Rater", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    content = models.CharField(max_length=260)