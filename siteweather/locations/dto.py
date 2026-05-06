from pydantic import BaseModel, field_validator, Field


class WeatherDTO(BaseModel):

    # ВАЖНО !!! добавь валидацию данных!!!
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
    def round_temperature(cls, value):
        return round(value)

    @field_validator("description")
    @classmethod
    def capitalize_text(cls, value):
        return value.capitalize()

    @field_validator("city")
    @classmethod
    def title_city(cls, value):
        return value.title()

    @field_validator("country")
    @classmethod
    def upper_country(cls, value):
        return value.upper()


class CreateLocationDTO(BaseModel):
    city: str
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)

    @field_validator("lat", "lon", mode="before")
    @classmethod
    def parse_coordinates(cls, value):
        if value is None:
            raise ValueError("Координата отсутствует")

        return float(str(value).replace(",", "."))