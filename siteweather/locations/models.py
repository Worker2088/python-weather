from django.db import models

from siteweather import settings


class Location(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6) # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6) # долгота

