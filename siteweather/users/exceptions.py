"""
Модуль содержит исключения связанные с локациями

"""

from core.exceptions import BaseAppException


class UserAlreadyExists(BaseAppException):
    pass
