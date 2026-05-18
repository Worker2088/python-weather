"""
Модуль для взаимодействия с внешним API OpenWeather.
Содержит функции для получения данных о погоде и преобразования их в DTO.
"""

import logging
from typing import Any

import requests
from pydantic import ValidationError
from requests import Timeout, HTTPError

from locations.dto import WeatherDTO
from locations.exceptions import (
    WeatherServiceUnavailable,
    CityNotFound,
    WeatherAPIError,
)
from django.conf import settings


logger = logging.getLogger(__name__)


def get_weather_api_openweather(city: str) -> WeatherDTO:
    """
    Получает данные о погоде для указанного города через OpenWeather API.

    Args:
        city (str): Название города.

    Returns:
        WeatherDTO: Объект с данными о погоде.

    Raises:
        WeatherServiceUnavailable: Если сервер погоды недоступен или произошел таймаут.
        CityNotFound: Если город не найден.
        WeatherAPIError: Если произошла ошибка при обработке ответа API.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    logger.info("получаем погоду для %s", city)

    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    try:
        response = requests.get(url, params=params, timeout=(3, 5))
        response.raise_for_status()
        # если сервер возвратил код ответа не 200,201,204, то выбрасывает raise requests.exceptions.HTTPError
        # и мы ловим и смотрим какой был код ответа

        response_dto = json_to_dto(response.json())

    except (Timeout, ConnectionError):
        logger.exception("сервер погоды не отвечает")
        raise WeatherServiceUnavailable()

    except HTTPError as e:
        status = e.response.status_code

        if status == 404:
            raise CityNotFound()

        logger.exception("ошибка HTTPError")
        raise WeatherServiceUnavailable()

    return response_dto


# mappers
def json_to_dto(weather_json: dict[str, Any]) -> WeatherDTO:
    """
    Преобразует JSON-ответ от OpenWeather API в объект WeatherDTO.

    Args:
        weather_json (dict[str, Any]): Словарь с данными ответа API.

    Returns:
        WeatherDTO: Объект с данными о погоде.

    Raises:
        WeatherAPIError: Если структура JSON не соответствует ожидаемой или возникла ошибка валидации.
    """
    logger.debug("преобразовываю JSON в ДТО")

    try:
        dto = WeatherDTO(
            temp=weather_json["main"]["temp"],
            feels_like=weather_json["main"]["feels_like"],
            city=weather_json["name"],
            country=weather_json["sys"]["country"],
            description=weather_json["weather"][0]["description"],
            icon=weather_json["weather"][0]["icon"],
            humidity=weather_json["main"]["humidity"],
            lon=weather_json["coord"]["lon"],
            lat=weather_json["coord"]["lat"],
        )
        logger.debug("преобразовал JSON в ДТО %s", dto)
        return dto
    except (KeyError, IndexError, TypeError, ValidationError) as e:
        logger.error("Некорректный ответ от API: %s", e)
        raise WeatherAPIError()
