from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import BankUserRegisterForm, BankUserLoginForm, TransferForm
from .models import BankUser, Transfer
from .utils import generate_suitable_transfers


def signup(request):
    if request.user.is_authenticated:
        return redirect(request, reverse('account'))

    if request.method == 'POST':
        form = BankUserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            mail = form.cleaned_data['email']
            password = form.cleaned_data['password']
            BankUser.objects.create_user(
                username, email=mail, password=password
            )
            messages.info(request, 'Konto utworzone, można się zarejstrować.')
            return redirect(reverse('login'))
    else:
        form = BankUserRegisterForm()
    return render(request, 'sign.html', {'form': form, 'btn_text': 'Zarejstruj'})


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
                messages.success(request, 'Zalogowano')
                return redirect(reverse('account'))
            else:
                messages.error(request, 'Nieprawidłowe dane logowania :/')
                return redirect(reverse('login'))
    else:
        form = BankUserLoginForm()
    return render(request, 'sign.html',
        {'form': form, 'btn_text': 'Zaloguj'}
    )


def transfer(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Wymagane zalogowanie się!')
        return redirect(reverse('index'))

    elif request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver']
            amount = abs(form.cleaned_data['amount'])

            if amount > request.user.available_founds:
                messages.error(request, 'Za mało środków :c')
                return redirect(reverse('account'))

            receiver = BankUser.objects.get(username=receiver_username)

            transfer = Transfer(
                amount=amount,
                sender=request.user,
                receiver=receiver
            )
            transfer.save()
            request.user.available_founds -= transfer.amount
            request.user.save()

            return redirect(
                reverse(
                    'show_transfer',
                    kwargs={'transfer_id': transfer.pk}
                )
            )
    else:
        form = TransferForm()
    
    return render(request, 'transfer.html', {'form': form})


def transfer_detail(request, transfer_id):
    transfer = get_object_or_404(Transfer, pk=transfer_id)
    if not request.user.is_authenticated  and request.user.is_sender():
        return redirect(reverse('account'))

    if request.method == 'POST':
        if request.POST.get('accepted', None):
            transfer.accept()
            return redirect(
                reverse(
                    'look_transfer',
                    kwargs={'transfer_id': transfer.pk}
                )
            )
        else:
            transfer.delete()
            return redirect(reverse('account'))
    else:
        return render(
            request,
            'transfer_detail.html',
            {'transfer': transfer, 'accept': True}
        )


def transfer_overview(request, transfer_id):
    transfer = get_object_or_404(Transfer, pk=transfer_id)
    if not request.user.is_authenticated  and request.user.is_sender():
        return redirect(reverse('account'))

    return render(
        request,
        'transfer_detail.html',
        {'transfer': transfer, 'accept': False}
    )


def signout(request):
    if request.user.is_authenticated:
        messages.success(request, 'Wylogowano!')
        logout(request)
    return redirect(reverse('index'))


def account(request):
    if request.user.is_authenticated:
        transfers, staged = generate_suitable_transfers(request.user)
        return render(
            request,
            'details.html',
            {
                'user': request.user,
                'transfers': transfers,
                'staged': staged,
            }
        )
    else:
        messages.ERROR(request, 'Wymagane zalogowanie się!')
        return redirect(reverse('index'))


def index(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, 'index.html', {'user': user})