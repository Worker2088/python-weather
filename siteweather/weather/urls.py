from django.urls import path

from weather import views

urlpatterns = [
    path('', views.index, name='home'),  # https://127.0.0.1:8000
]
