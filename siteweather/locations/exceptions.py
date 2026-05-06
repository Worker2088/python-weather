"""
Модуль содержит исключения связанные с локациями

"""

class BaseAppException(Exception): pass

class LocationAlreadyExists(BaseAppException): pass

class WeatherServiceUnavailable(BaseAppException): pass

class WeatherAPIError(BaseAppException): pass

class CityNotFound(BaseAppException): pass






