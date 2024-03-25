from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login as log
from django.contrib.auth import authenticate, logout

from .forms import *


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['login']
            email = form.cleaned_data['email']
            p1 = form.cleaned_data['password1']
            p2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Пользователь с таким логином уже существует!")
                return render(request, 'users/register.html', context={'form': form})

            if p1 != p2:
                messages.error(request, "Пароли не совпадают")
                return render(request, 'users/register.html', context={'form': form})
            else:

                new_user = User.objects.create_user(username=username, password=p1, email=email, first_name=first_name,
                                                    last_name=last_name)
                log(request, new_user)
                return HttpResponseRedirect("/posts")

    return render(request, 'users/register.html', context={'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            p = form.cleaned_data['password']
            user = authenticate(username=username, password=p)
            if user is not None:
                log(request, user)
                return HttpResponseRedirect("/posts")
            else:
                messages.error(request, 'Неправильно введен логин или пароль')
                return HttpResponseRedirect("/users/login")
        else:
            return HttpResponseRedirect("/users/login")

    else:
        form = LoginForm()
        return render(request, 'users/login.html', context={'login_form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/posts")