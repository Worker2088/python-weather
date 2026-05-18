"""
Модуль сервисного слоя для работы с локациями.
Содержит бизнес-логику для получения погоды, управления списком городов пользователя.
"""

import logging

from django.core.cache import cache

from locations.clients.openweather import get_weather_api_openweather
from locations.dto import WeatherDTO, CreateLocationDTO
from locations.exceptions import LocationAlreadyExists
from users.models import User
from locations.repository import LocationRepository


logger = logging.getLogger(__name__)


def get_weather(city: str) -> WeatherDTO:
    """
    Получает данные о погоде для указанного города.
    Сначала проверяет наличие данных в кэше, если их нет — запрашивает через API.

    Args:
        city (str): Название города.

    Returns:
        WeatherDTO: Объект с данными о погоде.
    """
    logger.info("начинаю получение погоды для %s", city)

    # кэширование, проверяю есть ли в город в кэше
    key = city.strip().lower()

    cached = cache.get(key)
    logger.info("ищу в кэшэ погоду для %s: %s", city, cache.get(key))

    if cached:
        logger.info("погода для %s ЕСТЬ в кэше, беру данные оттуда", city)
        return cached

    logger.info("погода для %s НЕТ в кэше, иду по АПИ", city)

    data = get_weather_api_openweather(city)

    # кэширование, добавляю город в кэш
    cache.set(key, data, timeout=20000)
    logger.debug("добавляю погоду в кэш для %s: %s", city, cached)

    return data


def get_all_cities_of_user(user: User) -> list[str]:
    """
    Возвращает список названий всех городов, добавленных пользователем.

    Args:
        user (User): Объект пользователя.

    Returns:
        list[str]: Список названий городов.
    """
    locs = LocationRepository.get_user_cities_repo(user)
    logger.debug("locs %s", locs)

    logger.info("список локаций для юзера %s", [loc.name for loc in locs])
    cities = []
    for loc in locs:
        # logger.debug("объект %s", loc.name)
        cities.append(loc.name)
    return cities


def delete_city(user: User, name_city: str) -> None:
    """
    Удаляет город из списка пользователя.

    Args:
        user (User): Объект пользователя.
        name_city (str): Название города для удаления.
    """
    logger.info(
        "вызван метод удаления города %s из базы данных %s", name_city, user.username
    )

    logger.debug("user=user %s name=city_name %s", user.username, name_city)
    LocationRepository.delete_city_repo(user=user, name_city=name_city)

    logger.info("удален города %s из базы данных юзера %s", name_city, user.username)


def add_city(user: User, location_dto: CreateLocationDTO) -> None:
    """
    Добавляет город в список пользователя.

    Args:
        user (User): Объект пользователя.
        location_dto (CreateLocationDTO): DTO с данными добавляемой локации.

    Raises:
        LocationAlreadyExists: Если город уже добавлен пользователем.
    """
    if LocationRepository.city_exists(user, location_dto.city):
        raise LocationAlreadyExists()

    LocationRepository.add_city_repo(user=user, dto=location_dto)

    logger.debug(
        "создал и сохранил объект Локация %s для юзера %s",
        location_dto.city,
        user.username,
    )
