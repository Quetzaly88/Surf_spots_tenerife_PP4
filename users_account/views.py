# import modules and classes
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import SurfSpot 
from .forms import RegistrationForm, SurfSpotForm

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  # for checking duplicate usernames
from django.views.decorators.http import require_POST


# User authentication views

#User registration view. Handles user registration and redirects to home. 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():  # check if form is valid, then save data to create user
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()  # if GET render empty form
    return render(request, 'users_account/register.html', {'form': form})  # render the registration template and pass the form instance to the template context.

# User login view. Handles user authentication and redirects to home.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users_account/login.html', {'error': "Invalid username or password"},)
    return render(request, 'users_account/login.html')

# User logout view. Logs out user and redirects to the login page
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

# Main applications views

# Home page view. Combines surf spot listing and creation in a single view. 
@login_required
def home_view(request):
    #Handle surf spot creation
    if request.method == 'POST':
        form = SurfSpotForm(request.POST)
        if form.is_valid():
            surf_spot = form.save(commit=False)
            surf_spot.user = request.user
            surf_spot.save()
            messages.success(request, "Surf spot created successfully!")
            return redirect('home')
    else:
        form = SurfSpotForm()

    # fetch and list all surf spots
    surf_spots = SurfSpot.objects.all().order_by('-created_at')
    return render(request, 'users_account/home.html', {'form': form, 'surf_spots': surf_spots})

# API endpoints

# API endpoint to list all surf spots in JSON format
def list_surf_spots(request): 
    if request.method == 'GET':
        spots = SurfSpot.objects.all().select_related('user').order_by('-created_at')
        data = [
            {
                "title": spot.title,
                "location": spot.location,
                "description": spot.description,
                "best_seasons": spot.best_seasons,
                "user": spot.user.username,
                "created_at": spot.created_at,
            }
            for spot in spots
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Error handlers

#unauthorized error handler. Returns a JSON response for unauthorized access
def error_unauthorized():
    return JsonResponse({'error': 'You must be logged in to perform thisaction'}, status=401)