from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


class LoginForm(AuthenticationForm):
    """Форма для логина пользователя"""

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'password')

    def is_valid(self):
        """Аутентификация пользователя по email и password"""

        email = self.data.get('email')
        password = self.data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)

            return redirect('main:index')


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        """Проверка на уникальность поля email по БД"""

        email = self.cleaned_data['email']
        records = User.objects.filter(email=email)
        if records:
            raise ValidationError('Пользователь с таким email уже существует')

        return email
