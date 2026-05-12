"""
Модуль содержит исключения связанные с локациями

"""
from core.exceptions import BaseAppException


class LocationAlreadyExists(BaseAppException): pass

class WeatherServiceUnavailable(BaseAppException): pass

class WeatherAPIError(BaseAppException): pass

class CityNotFound(BaseAppException): pass






