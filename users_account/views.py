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
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import necessary classes for pagination


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
        #user = None #Inilialize user to avoid unboundlocalerror
        user = authenticate(request, username=username, password=password)
        #print(f"Authentication attempted: {username}, {password}, User: {user}")  # Debugging
        if user is not None:
            login(request, user)
            #print("User logged in, redirecting to home.")  # Debugging
            return redirect('home')
        else:
            #print("Invalid login.")  # Debugging
            return render(request, 'users_account/login.html', {'error': "Invalid username or password"})
    return render(request, 'users_account/login.html')

# User logout view. Logs out user and redirects to the login page
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

# Main applications views

# Home page view. Combines surf spot listing and creation in a single view. 
@login_required
def home_view(request):
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

    # fetch and list all surf spots to display on the homepage
    surf_spots = SurfSpot.objects.all().order_by('-created_at')
    return render(request, 'users_account/home.html', {'form': form, 'surf_spots': surf_spots})

# API endpoints

#API endpoint to create a surf spot
@login_required
@require_http_methods(["POST"])
def create_surf_spot_api(request):
    form = SurfSpotForm(json.loads(request.body)) #Parse JSON request body
    if form.is_valid():
        surf_spot = form.save(commit=False) # create surf spot without saving
        surf_spot.user = request.user # assign current user to the surf spot
        surf_spot.save() #save to the database
        return JsonResponse({'message': 'Surf spot created successfully!'}, status=201)
    return JsonResponse({'errors': form.errors}, status=400) #return validation errors

# API endpoint to list all surf spots
@login_required
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

# API endpoint to list surf spots with pagination
@login_required
def list_surf_spots_paginated(request):
    """
    View to list surf spots with pagination. Returns Json response 
    with paginated surf spots data
    """
    page_number = request.GET.get('page', 1) #default from request query parameters
    posts_per_page = 5
    surf_spots = SurfSpot.objects.all().order_by('-created_at') #query database for all SurfSpot objects
    paginator = Paginator(surf_spots, posts_per_page)

    try:
        spots_page = paginator.page(page_number) # Get the requested page of surf spots
    except PageNotAnInteger:
        #if page is not an integer, return the first page
        spots_page = paginator.page(1)
    except EmptyPage:
        # if page is out of range, return an empty page
        return JsonResponse({'error': 'No more posts avaiable'}, status=404)

    # Prepare the data for the JSON response
    data = [
        {
            'id': spot.id,
            'title': spot.title,
            'location': spot.location,
            'created_at': spot.created_at.strftime('%Y-%m-%d'),
        }
        for spot in spots_page
    ]

    # Return the paginated data along with metadata
    return JsonResponse({
        'surf_spots': data, 
        'total_pages': paginator.num_pages,
        'current_page': spots_page.number,
        'has_next': spots_page.has_next(),
        'has_previous': spots_page.has_previous(),
    })



# Error handlers

# Custom 404 error handler
def custom_404(request, exception):
    return render(request, '404.html', status=404)  # Render custom 404 page

# Custom 500 error handler
def custom_500(request):
    return render(request, '500.html', status=500)  # Render custom 500 page