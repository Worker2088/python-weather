"""
Модуль представлений для приложения users.
Использует стандартные классы Django для авторизации и регистрации.
"""

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from users.exceptions import UserAlreadyExists
from users.forms import CustomLoginForm, RegisterUserForm
from users.services import AuthService


class CustomLoginView(LoginView):
    """
    Представление для входа пользователя в систему.
    """
    template_name = 'users/sign-in.html'
    authentication_form = CustomLoginForm


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    """
    form_class = RegisterUserForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('locations:home')

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        """
        Обрабатывает корректно заполненную форму регистрации.
        Регистрирует пользователя через AuthService и выполняет автоматический вход.

        Args:
            form (RegisterUserForm): Валидная форма регистрации.

        Returns:
            HttpResponse: Редирект на главную страницу при успехе или повторное отображение формы при ошибке.
        """
        try:
            user = AuthService.register_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
        except UserAlreadyExists:
            messages.error(self.request, "пользователь с таким именем уже есть существует")
            return self.form_invalid(form)

        self.object = user
        # автологин после реги
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())
