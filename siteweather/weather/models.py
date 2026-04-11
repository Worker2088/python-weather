from django.db import models

class User(models.Model):
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=25)


class Location(models.Model):
    name = models.CharField(max_length=25)
    user_id = models.IntegerField()
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="locations"
    # )
    latitude = models.DecimalField(max_digits=9, decimal_places=6) # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6) # долгота

