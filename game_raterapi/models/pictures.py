from django.db import models


class Picture(models.Model):

    rater = models.ForeignKey("Rater", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)