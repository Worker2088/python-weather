import pytest
import responses
from django.conf import settings

from locations.exceptions import CityNotFound
from locations.services import get_weather
from locations.dto import WeatherDTO


@pytest.mark.django_db
class TestWeatherIntegration:

    # перехватываю HTTP-запросы через библиотеку responses и подменяю их моками
    @responses.activate
    def test_find_location_by_name_success(self, openweather_success_data):
        """Проверка успешной цепочки: Service -> Client -> HTTP Mock -> DTO"""
        # 1. Arrange: Настраиваем перехват запроса
        # URL должен совпадать с тем, что формирует ваш клиент
        search_name = "Moscow"
        api_url = "https://api.openweathermap.org/data/2.5/weather"

        # создаем мок, далее если URL и метод совпали то возвращается поддельный ответ
        responses.add(
            method=responses.GET,
            url=api_url,
            json=openweather_success_data,
            status=200
        )

        # 2. Act
        locations = get_weather(search_name)

        # 3. Assert
        assert isinstance(locations, WeatherDTO)
        assert locations.city == "Moscow"
        assert locations.lat == 55.7522
        # Проверяем, что был сделан ровно один запрос
        assert len(responses.calls) == 1


    @responses.activate
    def test_find_location_api_returns_error(self):
        """Проверка обработки 4xx/5xx ошибок от внешнего сервиса"""
        # 1. Arrange
        api_url = "https://api.openweathermap.org/data/2.5/weather"
        responses.add(
            method=responses.GET,
            url=api_url,
            status=404,  # город не найден
            json={"message": "город не найден"}
        )

        # 2. Act & Assert
        # Мы ожидаем, что сервис обернет ошибку клиента в наше системное исключение
        with pytest.raises(CityNotFound):
            get_weather("Moscow123")