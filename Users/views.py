from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from Marking.mixin import BaseClassContextMixin
from .forms import *


# Create your views here.


class UserLogout(LogoutView, BaseClassContextMixin):
    model = User
    template_name = 'Users/logout.html'
    success_url = reverse_lazy('Users:login')


class UserLogin(LoginView, BaseClassContextMixin):
    model = User
    form_class = UserLoginForm
    template_name = 'Users/login.html'
    success_url = reverse_lazy('Main:index')
    title = 'Авторизация'

    def post(self, request, *args, **kwargs):
        auth = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not auth:
            messages.error(request, 'Некорректное имя пользователя или пароль!')
            return redirect('Users:login')
        login(request, auth)
        if auth.is_active:
            return redirect(self.success_url)
        else:
            messages.error(request, 'Пользователь отключен.')
            return redirect('Users:login')

