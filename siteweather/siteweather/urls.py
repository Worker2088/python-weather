"""
Конфигурация корневых URL проекта siteweather.
Включает в себя маршруты админки и маршруты приложений locations и users.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('locations.urls')),
    path('users/', include('users.urls')),
]
