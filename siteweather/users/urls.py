"""
Конфигурация URL для приложения users.
Определяет маршруты для входа, выхода и регистрации пользователей.
"""

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.views import CustomLoginView, RegisterView

# namespace
app_name = 'users'

urlpatterns = [
    # path('', views.index, name='home'),  # https://127.0.0.1:8000
    # path('sign-in/', views.sign_in, name='sign-in'),
    # path('logout/', views.sign_out, name='logout'),
    # path('sign-in/', LoginView.as_view(template_name='users/sign-in.html'), name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', RegisterView.as_view(), name='sign-up'),
]
