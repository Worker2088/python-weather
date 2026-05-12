import pytest
from django.contrib.auth import get_user_model

from users.exceptions import UserAlreadyExists
from users.services import AuthService


User = get_user_model()


@pytest.mark.django_db
class TestAuthService:

    def test_registration_creates_user_in_db(self):
        """Проверка, что вызов сервиса создает запись в таблице Users"""
        # 1. Arrange (Подготовка)
        auth_service = AuthService()

        # 2. Act (Действие)
        user = auth_service.register_user("tester", "safe_password")

        # 3. Assert (Проверка)
        assert User.objects.filter(username="tester").exists()
        assert user.username == "tester"

    def test_registration_fails_on_duplicate_username(self):
        """Проверка обработки неуникального логина"""
        auth_service = AuthService()

        # Создаем первого пользователя
        auth_service.register_user("duplicate", "password123")

        # Пытаемся создать второго с тем же именем
        with pytest.raises(UserAlreadyExists):
            auth_service.register_user("duplicate", "password123")

