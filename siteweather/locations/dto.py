"""
Модуль DTO (Data Transfer Objects) для приложения locations.
Использует Pydantic для валидации и структурирования данных.
"""

from typing import Any
from pydantic import BaseModel, field_validator, Field


class WeatherDTO(BaseModel):
    """
    DTO для хранения и валидации данных о погоде, полученных из API.
    """

    temp: float
    feels_like: float
    city: str
    country: str
    description: str
    icon: str
    humidity: int = Field(ge=0, le=100)
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)

    @field_validator("temp", "feels_like")
    @classmethod
    def round_temperature(cls, value: float) -> int:
        """Округляет значение температуры."""
        return round(value)

    @field_validator("description")
    @classmethod
    def capitalize_text(cls, value: str) -> str:
        """Приводит описание к верхнему регистру в начале строки."""
        return value.capitalize()

    @field_validator("city")
    @classmethod
    def title_city(cls, value: str) -> str:
        """Приводит название города к формату заголовка."""
        return value.title()

    @field_validator("country")
    @classmethod
    def upper_country(cls, value: str) -> str:
        """Приводит код страны к верхнему регистру."""
        return value.upper()


class CreateLocationDTO(BaseModel):
    """
    DTO для валидации данных при создании новой локации.
    """

    city: str
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)

    @field_validator("lat", "lon", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> float:
        """
        Преобразует входное значение координаты в float, обрабатывая запятые.
        """
        if value is None:
            raise ValueError("Координата отсутствует")

        return float(str(value).replace(",", "."))

    @field_validator("city", mode="before")
    @classmethod
    def parse_city(cls, value: Any) -> str:
        """
        Преобразует входное значение названия города в строку, проверяет на None.
        """
        if value is None:
            raise ValueError("Название города отсутствует")

        return str(value)
