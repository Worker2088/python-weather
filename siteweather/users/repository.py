from django.contrib.auth import get_user_model


User = get_user_model()


class UserRepository:

    @staticmethod
    def create_user(username: str, password: str) -> User:
        """
        Создание пользователя через Django form.
        """
        return User.objects.create_user(
        username=username,
        password=password
        )

