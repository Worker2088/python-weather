import logging

from locations.dto import CreateLocationDTO
from locations.models import Location
from users.models import User

logger = logging.getLogger(__name__)

class LocationRepository:

    @staticmethod
    def city_exists(user: User, city: str) -> bool:
        return Location.objects.filter(user=user, name=city).exists()

    @staticmethod
    def add_city_repo(user: User, dto: CreateLocationDTO) -> Location:
        return Location.objects.create(
            user=user,
            name=dto.city,
            latitude=dto.lat,
            longitude=dto.lon
        )

    @staticmethod
    def get_user_cities_repo(user: User) -> list[Location]:
        return Location.objects.filter(user=user)

    @staticmethod
    def delete_city_repo(user: User, name_city: str) -> None:
        logger.debug("user %s city %s", user.username, name_city)
        return Location.objects.filter(user=user, name=name_city).delete()