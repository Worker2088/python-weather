"""
ASGI конфигурация для проекта siteweather.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweather.settings.production')

application = get_asgi_application()
