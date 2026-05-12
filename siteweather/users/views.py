from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages


from users.exceptions import UserAlreadyExists
from users.forms import CustomLoginForm, RegisterUserForm
from users.services import AuthService


# заменяем метод def sign_in(request) на этот класс
class CustomLoginView(LoginView):
    template_name = 'users/sign-in.html'
    authentication_form = CustomLoginForm


# заменяем метод def sign_up(request) на этот класс
# для того чтобы использовать встроенную Django архитектуру без самописного кода авторизации
class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('locations:home')

    def form_valid(self, form):

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



# def sign_up(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#
#         if form.is_valid():
#             form.save()  # ← ВСЁ, этого достаточно
#             # return render(request, 'locations/index.html')
#             return redirect('locations:home')
#     else:
#         form = RegisterUserForm()
#
#     return render(request, 'users/sign-up.html', {'form': form})

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

