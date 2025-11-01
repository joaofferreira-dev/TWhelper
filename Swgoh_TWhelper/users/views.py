
from django.shortcuts import render, redirect
from django.contrib import messages
# from TWhelper.forms import UserRegisterForm
#from account.forms import PasswordChangeForm
from .forms import UserRegisterForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            # Changes newly created user status to not active
            User.objects.filter(username=username).update(is_active=False)

            messages.success(request, f'Account created for {username}! AWAIT activation!')
            return redirect('TWhelper-home')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':

        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            username = request.user.username

            messages.success(request, f'Password changed for {username}!!')
            return redirect('TWhelper-teams')

    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change-password.html', {'form': form})
