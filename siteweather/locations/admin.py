"""
Конфигурация админки для приложения locations.
"""

from django.contrib import admin
from .models import Location

admin.site.register(Location)
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Приложение Погода"
