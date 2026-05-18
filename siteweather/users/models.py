"""
Модуль моделей для приложения users.
Определяет кастомную модель пользователя.
"""

from django.contrib.auth.models import AbstractUser

# создаем свою табл User, наследуемся от AbstractUser где уже есть базовые нужные поля
# поэтому не прописываем их в классе
class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    pass
