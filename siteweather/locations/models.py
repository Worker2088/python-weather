"""
Модуль моделей для приложения locations.
Определяет структуру данных для хранения локаций пользователей.
"""

from django.db import models
from django.conf import settings


class Location(models.Model):
    """
    Модель локации (города), привязанной к пользователю.
    """

    name = models.CharField(max_length=25)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота

    def __str__(self) -> str:
        """Возвращает строковое представление локации."""
        return f"{self.name} ({self.user.username})"
