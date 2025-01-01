# import modules and classes
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import SurfSpot 
from django.contrib import messages  # displays messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # for checking duplicate usernames
from django.views.decorators.http import require_POST
from .forms import RegistrationForm  # Custom form class for user registration.
from .forms import SurfSpotForm


# register view for user registration
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
            return render(request, 'users_account/login.html', {'error': "Invalid username or password"},)
    return render(request, 'users_account/login.html')

# logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

# Home page view
@login_required
def home_view(request):
    return render(request, 'users_account/home.html')

# create_surf_spot API endpoint to handle post creation and include validation and error handling. 
@login_required
def create_surf_spot(request): 
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
    
    return render(request, 'surf_spots/create_surf_spot.html', {'form': form})

# API endpoint to List surf spots 
def list_surf_spots(request):
    if request.method == 'GET':
        # query all surf spots, including related user data, sorted by creation date. 
        spots = SurfSpot.objects.all().select_related('user').order_by('-created_at')
        
        # Prepare serialized data for JSON response
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

        #return serialized data as JSON
        return JsonResponse(data, safe=False)

    #return error response for invalid reques methods
    return JsonResponse({'error': 'Invalid request method'}, status=405)

#unauthorized error handler
def error_unauthorized():
    return JsonResponse({'error': 'You must be logged in to perform thisaction'}, status=401)