from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, RegistrationForm
from .mixins import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    """Логин пользователя"""

    form_class = LoginForm
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('main:index')
    title = 'Авторизация'


class UserRegistrationView(TitleMixin, CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = RegistrationForm
    template_name = 'app_users/registration.html'
    success_url = reverse_lazy('users:sign-in')
    title = 'Регистрация'

    def form_valid(self, form):
        """Добавляем email в поле формы username"""

        form.instance.username = form.cleaned_data.get('email')

        return super().form_valid(form)
