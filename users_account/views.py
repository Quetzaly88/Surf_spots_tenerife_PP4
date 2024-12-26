# import modules and classes
from django.shortcuts import (
    render,
    redirect,
)  # renders HTML templates, redirects to a different URL
from django.contrib import messages  # displays messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # for checking duplicate usernames
from .forms import RegistrationForm  # Custom form class for user registration.


# register view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():  # check if form is valid, then save data to create user
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()  # if GET render empty form
    return render(
        request, 'users_account/register.html', {'form': form}
    )  # render the registration template and pass the form instance to the template context.

    # login view


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users_account/login.html', {'error': "Invalid username or password"},
            )
    return render(request, 'users_account/login.html')


# logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page


# create post view. @login_required decorator, to limit access just to logged-in users
@login_required
def home_view(request):
    return render(request, 'users_account/home.html')


# create home page
@login_required
def home_view(request):
    return render(request, 'users_account/home.html')
