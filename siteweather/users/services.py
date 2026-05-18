"""
Модуль сервисного слоя для работы с пользователями.
Содержит бизнес-логику для аутентификации и регистрации.
"""

from django.db import IntegrityError

from users.exceptions import UserAlreadyExists
from users.models import User
from users.repository import UserRepository


class AuthService:
    """
    Класс-сервис для обработки операций аутентификации и регистрации.
    """

    @staticmethod
    def register_user(username: str, password: str) -> User:
        """
        Регистрирует нового пользователя в системе.

        Args:
            username (str): Логин пользователя.
            password (str): Пароль пользователя.

        Returns:
            User: Созданный объект пользователя.

        Raises:
            UserAlreadyExists: Если пользователь с таким логином уже существует.
        """
        try:
            user = UserRepository.create_user(
                username=username,
                password=password
            )
        except IntegrityError:
            raise UserAlreadyExists()

        return user
