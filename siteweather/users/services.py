from django.contrib.auth import login
from django.db import IntegrityError

from users.exceptions import UserAlreadyExists
from users.repository import UserRepository


class AuthService:

    @staticmethod
    def register_user(username, password):
        """
        Регистрация пользователя.
        """
        try:
            user = UserRepository.create_user(
                username=username,
                password=password
            )
        except IntegrityError:
            raise UserAlreadyExists()

        return user