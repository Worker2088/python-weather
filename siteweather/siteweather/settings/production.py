"""
Настройки для прода.
"""

from .base import *

# 1. Безопасность (важно!)
DEBUG = False

# Считываем SECRET_KEY из окружения.
# В продакшене приложение должно падать, если ключ не задан.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# Список доменов, на которых работает приложение
# Пример: weather.com,api.weather.com
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# 2. Настройки безопасности HTTP/SSL
# Говорим Django, что если Nginx передал заголовок X-Forwarded-Proto: https,
# значит запрос безопасен.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Редирект с http на https
SECURE_SSL_REDIRECT = False

# Защита кук: передавать только по HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (Strict-Transport-Security) — заставляет браузер всегда использовать HTTPS
SECURE_HSTS_SECONDS = 0  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Защита от XSS и встраивания во фреймы
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# 3. База данных (Production конфигурация)
# Полагаемся на переменные окружения, которые передает Docker Compose
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 600,  # Повторное использование соединений (Performance)
    }
}

# 4. Статика и Медиа
# В проде файлы должен отдавать Nginx. STATIC_ROOT указывает, куда собрать файлы.
STATIC_ROOT = BASE_DIR / "staticfiles"
# Включаем WhiteNoise или аналоги, если Nginx не используется для статики (редко для Django)
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# 5. Логирование (Production уровень)
# Отключаем вывод в консоль, переходим к структурированным логам в файл или Sentry
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/data.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
