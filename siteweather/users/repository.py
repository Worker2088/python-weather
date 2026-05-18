"""
Модуль репозитория для работы с моделью User.
Предоставляет методы для работы с пользователями в базе данных.
"""

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository:
    """
    Класс-репозиторий для выполнения операций с моделью User.
    """

    @staticmethod
    def create_user(username: str, password: str) -> User:
        """
        Создает нового пользователя.
        """
        return User.objects.create_user(
        username=username,
        password=password
        )
