# import modules and classes
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import SurfSpot, Comment, ModerationLog
from .forms import RegistrationForm, SurfSpotForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  # for checking duplicate usernames
from django.views.decorators.http import require_http_methods

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import necessary classes for pagination
from django.shortcuts import get_object_or_404 # import get_object_or_404 for fetching a specific post or returning 404

import logging

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
    """
    Handles listing and creation of surf spots. 
    Support pagination for listing surf spots
    """
    if request.method == 'POST':
        form = SurfSpotForm(request.POST)
        if form.is_valid():
            surf_spot = form.save(commit=False)
            surf_spot.user = request.user
            surf_spot.save()
            messages.success(request, "Surf spot created successfully!")
            return redirect('home')
        else:
            print(form.errors) #debugging
    else:
        form = SurfSpotForm()

    #Fetch category filter request
    selected_category = request.GET.get('category')
    print(f"Raw selected category: {selected_category}")

    #Initialize surf_spots_list based wether a category is selected.
    if selected_category:
    # fetch all surf spots and order by creation date
        surf_spots_list = SurfSpot.objects.filter(category=selected_category).order_by('-created_at')
        print(f"Selected category: {selected_category}, Surf spots found: {surf_spots_list.count()}") #debugging
    else:
        surf_spots_list = SurfSpot.objects.all().order_by('-created_at')
        print(f"No category selected, Total surf spots: {surf_spots_list.count()}") #debugging

    # Paginate the surf spots list, 5 spots per page
    paginator = Paginator(surf_spots_list, 5) # ensured that is set to 5
    page_number = request.GET.get('page')
    surf_spots = paginator.get_page(page_number)

    #render the homepage template with the formand paginated surfspots
    return render(request, 'users_account/home.html', {
        'form': form, 
        'surf_spots': surf_spots,
        'selected_category': selected_category,
    })


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


#API endpoint to fetch the details of a specific surf spot
@login_required # Without this not-logged in users can VIEW the posts and comments. Other changes can be made in the future. 
def surf_spot_detail(request, spot_id):
    """
    View to fetch details of a specific surf spot.
    Renders template with post details instead of Json response.
    """
    #Fetch the specific surf spot by its ID. Return 404 if not found. 
    surf_spot = get_object_or_404(SurfSpot, id=spot_id)
    #render the detail view template
    return render(request, 'users_account/surf_spot_detail.html', {'surf_spot': surf_spot})

# Add a view for Comment Creation
@login_required # Just logged in users can view posts and comments
@require_http_methods(["POST"])
def add_comment(request, spot_id):
    """
    View to handle comment creation. 
    Just for logged in users
    """
    surf_spot = get_object_or_404(SurfSpot, id=spot_id) #fetch the surf spot or show error 404
    form = CommentForm(request.POST)

    if form.is_valid():
        # Create a new comment but don't save the database yet
        comment = form.save(commit=False)
        comment.surf_spot = surf_spot # Associate the comment with the logged-in user
        comment.user = request.user # Associate comment with the logged in user
        comment.save() # Save the comment to the database 
        messages.success(request, "Comment added successfully!")
        return redirect('surf_spot_detail', spot_id=spot_id)
    else: 
        messages.error(request, "Failed to add comment. Please, check your message.")
        # Re-render the detail page with the existing comments and the form with errors.
        comments = surf_spot.comments.all().order_by('-created_at')
        return render(request, 'users_account/surf_spot_detail.html', {
            'surf_spot': surf_spot,
            'comment_form': form,
            'comments': comments,
        })
    
    # Redirect back to the surf spot detail page

# Error handlers

# Custom 404 error handler
def custom_404(request, exception):
    return render(request, '404.html', status=404)  # Render custom 404 page

# Custom 500 error handler
def custom_500(request):
    return render(request, '500.html', status=500)  # Render custom 500 page

# User story6
# Set up a logger framework to log admin actions / deletions. 
logger = logging.getLogger(__name__)

@login_required
def delete_post(request, post_id):
    """
    View to handle deletion of a surf spot post.
    Admins can delete any post. Regular users can only delete their own posts.
    """
    post = get_object_or_404(SurfSpot, id=post_id)

    if request.user.is_superuser or post.user == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")

        if request.user.is_superuser:
            # Log the modetarion action
            ModerationLog.objects.create(
            action_type ="Deleted Post",
            moderator=request.user,
            target_user=post.user.username,
            target_content=post.title,
            )
            logger.info(f"Admin {request.user.username} deleted post '{post.title}'")
    else:
        messages.error(request, "You are not authorized to delete this post.")
        
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    """
    View to handle deletion of a comment.
    Admins can delete any comment. Regular users can only delete their own comments.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_superuser or comment.user == request.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")

        if request.user.is_superuser:
            # Log the moseration action
            ModerationLog.objects.create(
            action_type ="Deleted Comment",
            moderator=request.user,
            target_user=comment.user.username,
            target_content=comment.content[:50],
            )
            logger.info(f"Admin {request.user.username} deleted comment by {comment.user.username}")
    else:
        messages.error(request, "You are not authorized to delete this comment.")
        
    return redirect('home')
    

    