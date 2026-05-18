"""
Конфигурация pytest для всего проекта.
Содержит общие фикстуры для тестов.
"""

from typing import Any

import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Автоматически разрешает всем тестам доступ к базе данных.
    Django-pytest по умолчанию изолирует тесты от БД.
    """
    pass


# @pytest.fixture
# def user_service():
#     """
#     Фикстура для сервиса пользователей (заглушка).
#     """
#     # Импортируй свой класс сервиса здесь
#     # return UserService()
#     pass


@pytest.fixture
def openweather_success_data() -> dict[str, Any]:
    """
    Валидный ответ от OpenWeather Weather API (/data/2.5/weather).
    ВАЖНО: Это должен быть словарь, а не список.
    """
    return {
        "name": "Moscow",
        "coord": {"lat": 55.7522, "lon": 37.6156},
        "sys": {"country": "RU"},
        "main": {"temp": 4.26, "feels_like": 1.61, "humidity": 49},
        "weather": [{"description": "overcast clouds", "icon": "04d"}],
    }
