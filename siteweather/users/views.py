import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomLoginForm, RegisterUserForm


# from users.forms import LoginUserForm

# заменяем метод def sign_in(request) на этот класс
# для того чтобы использовать встроенную Django архитектуру без самописного кода авторизации
class CustomLoginView(LoginView):
    template_name = 'users/sign-in.html'
    authentication_form = CustomLoginForm

# def sign_in(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST) # создаю словарь с полями формы
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user) # создаю сессию и юзер считается залогиненным
#                 return redirect('locations:home')
#             else:
#                 form.add_error(None, 'Неверный логин или пароль')
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/sign-in.html', {'form': form})

# заменяем метод def sign_up(request) на этот класс
# для того чтобы использовать встроенную Django архитектуру без самописного кода авторизации
class RegisterView(CreateView):
    # используем нашу форму RegisterUserForm когда надо добавить доп.поля в регистрацию
    form_class = RegisterUserForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('locations:home')

    # автологин после реги
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

def sign_up(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()  # ← ВСЁ, этого достаточно
            # return render(request, 'locations/index.html')
            return redirect('locations:home')
    else:
        form = RegisterUserForm()

    return render(request, 'users/sign-up.html', {'form': form})



