from django.urls import path

from locations import views

app_name = "locations"

urlpatterns = [
    path("", views.index, name="home"),  # https://127.0.0.1:8000
    path("add/", views.add, name="add"),
    path("delete/", views.delete, name="delete"),
    path("search-results/", views.search, name="search-results"),
]
