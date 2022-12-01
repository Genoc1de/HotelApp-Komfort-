from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя', max_length=30, required=False, help_text='Необязательно')
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False, help_text='Необязательно')
    email = forms.EmailField(label='Электронная почта', max_length=254,help_text='Обязательно для заполнения.Введите действующий адрес электронной почты.')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


