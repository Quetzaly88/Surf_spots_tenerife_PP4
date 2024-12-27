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

# create home page
@login_required
def home_view(request):
    return render(request, 'users_account/home.html')


#Create a surf spot
# add API endpoint to handle post creation in views.py. 
# template. https://medium.com/@jacobtamus/create-basic-get-post-endpoints-with-django-rest-framework-e3ef5721e5d
@csrf_exempt
@login_required
def create_surf_spot(request):
    try: 
        if request.method == 'POST':
            data = json.loads(request.body)
            title = data.get('title')
            location = data.get('location')
            description = data.get('description')
            best_seasons = data.get('best_seasons', '')

        #validate required fields
            if not title or not location or not description:
                return JsonResponse({'error': 'All required fields must be filled'}, status=400)

        #save the surf spot
            surf_spot = SurfSpot.objects.create(
                title=title,
                location=location, 
                description=description,
                best_seasons=best_seasons,
                user=request.user,
            )
            return JsonResponse({'message': "Surf spot created successfully"}, status=201)


        return JsonResponse({'error': "Invalid request method"}, status=405)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


# List surf spots 
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


def error_unauthorized():
    return JsonResponse({'error': 'You must be logged in to perform thisaction'}, status=401)