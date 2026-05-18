"""
Модуль представлений (views) для приложения locations.
Обрабатывает HTTP-запросы для отображения главной страницы, поиска, добавления и удаления городов.
"""

import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from pydantic import ValidationError

from .dto import CreateLocationDTO
from .exceptions import LocationAlreadyExists, WeatherServiceUnavailable, CityNotFound, WeatherAPIError
from .services import add_city, get_all_cities_of_user, delete_city, get_weather

logger = logging.getLogger(__name__)


def index(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу."""
    cities_dto_list = []

    if request.user.is_authenticated:
        cities_name_list = get_all_cities_of_user(request.user)

        try:
            for city in cities_name_list:
                city_dto = get_weather(city)
                cities_dto_list.append(city_dto)

        except WeatherServiceUnavailable:
            messages.error(request, "Сервис погоды временно недоступен, попробуйте позже")

        except WeatherAPIError:
            messages.error(request, "Некорректный ответ от API")

        except CityNotFound:
            messages.error(request, f"Город {city} не найден, поправь название")

    return render(request, "locations/index.html", {
        "cities": cities_dto_list
    })


@login_required
@require_POST
def delete(request: HttpRequest) -> HttpResponse:
    """Удаляет город из списка."""
    logger.debug("получил запрос от юзера %s на удаление %s", request.user.username, request.POST.get("city_name"))
    city_name = request.POST.get("city_name")

    try:
        if not city_name:
            messages.error(request, "Город для удаления не указан")
            return redirect("locations:home")

        delete_city(request.user, city_name)
        messages.success(request, f"Город {city_name} успешно удален из вашего списка")

    except CityNotFound:
        messages.error(request, "Не удалось удалить город")

    return redirect("locations:home")


def add(request: HttpRequest) -> HttpResponse:
    """Добавляет город в список."""

    if not request.user.is_authenticated:
        return redirect("users:sign-in")

    if request.method != "POST":
        return redirect('locations:home')

    logger.debug("начинаю добавлять локацию %s для юзера %s", request.POST.get("city"), request.user.username)

    try:
        city = request.POST.get("city")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        dto = CreateLocationDTO(
            city=city,
            lat=lat,
            lon=lon,
        )

        add_city(request.user, dto)
        messages.success(request, f"Город {dto.city} добавлен в список")

    except ValidationError as e :
        msg = e.errors()[0]["msg"]
        messages.error(request, msg)
        return redirect("locations:search-results")

    except LocationAlreadyExists:
        messages.warning(request, f"Город {dto.city} уже есть в списке")

    return redirect('locations:home')


def search(request: HttpRequest) -> HttpResponse:
    """Выполняет поиск города."""
    city = request.GET.get("name")
    data = None

    if not city:
        return render(request, "locations/search-results.html")

    try:
        data = get_weather(city)

    except CityNotFound:
        messages.error(request, f"Город {city} не найден, поправь название")

    except WeatherServiceUnavailable:
        messages.error(request, "Сервис погоды временно недоступен, попробуйте позже")

    return render(request, "locations/search-results.html", {
            "data": data,
            "city": city
        })
