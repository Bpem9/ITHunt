from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

class UserRegForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder':'Логин', 'area-label': 'Логин', 'aria-describedby': "basic-addon1"}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder':'E-mail', 'area-label': 'E-mail', 'aria-describedby': "basic-addon1"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control is-invalid', 'type': 'text', 'placeholder':'Пароль', 'area-label': 'Пароль', 'aria-describedby': "basic-addon1"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control is-invalid', 'type': 'text', 'placeholder':'Повторите пароль', 'area-label': 'Повторите пароль', 'aria-describedby': "basic-addon1"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={}))