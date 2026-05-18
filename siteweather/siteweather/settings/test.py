"""
Настройки для запуска тестов.
Использует sqlite3 в памяти и фиктивные кэши для ускорения выполнения.
"""

from .base import *

DEBUG = False

# Используем быстрый хешер для тестов
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # или файл
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


SESSION_COOKIE_AGE = 1800
