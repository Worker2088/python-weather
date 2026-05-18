"""
Модуль репозитория для работы с моделью Location.
Интерфейс для взаимодействия с базой данных по вопросам локаций пользователей.
"""

import logging
from typing import Tuple, Dict

from locations.dto import CreateLocationDTO
from locations.models import Location
from users.models import User

logger = logging.getLogger(__name__)

class LocationRepository:
    """
    Класс-репозиторий для выполнения CRUD операций с моделью Location.
    """

    @staticmethod
    def city_exists(user: User, city: str) -> bool:
        """Проверяет существование города в списке пользователя."""
        return Location.objects.filter(user=user, name=city).exists()

    @staticmethod
    def add_city_repo(user: User, dto: CreateLocationDTO) -> Location:
        """Добавляет новый город в БД."""
        return Location.objects.create(
            user=user,
            name=dto.city,
            latitude=dto.lat,
            longitude=dto.lon
        )

    @staticmethod
    def get_user_cities_repo(user: User) -> list[Location]:
        """Получает все города пользователя."""
        return list(Location.objects.filter(user=user))

    @staticmethod
    def delete_city_repo(user: User, name_city: str) -> Tuple[int, Dict[str, int]]:
        """Удаляет город из БД."""
        logger.debug("user %s city %s", user.username, name_city)
        return Location.objects.filter(user=user, name=name_city).delete()
