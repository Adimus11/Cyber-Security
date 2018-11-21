from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import BankUserRegisterForm, BankUserLoginForm
from .models import BankUser


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('account'))

    if request.method == 'POST':
        form = BankUserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            mail = form.cleaned_data['email']
            password = form.cleaned_data['password']
            BankUser.objects.create_user(
                username, email=mail, password=password
            )
            return redirect(reverse('login'))
    else:
        form = BankUserRegisterForm()
    return render(request, 'sign.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect(reverse('account'))

    if request.method == 'POST':
        form = BankUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            print(username, raw_password)
            user = authenticate(
                request, username=username, password=raw_password
            )
            if user is not None:
                login(request, user)
                return redirect(reverse('account'))
            else:
                return redirect(reverse('index'))
    else:
        form = BankUserLoginForm()
    return render(request, 'sign.html', {'form': form})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('account'))


def account(request):
    if request.user.is_authenticated:
        return render(request, 'details.html', {'user': request.user})
    else:
        return redirect(reverse('index'))


def index(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, 'index.html', {'user': user})