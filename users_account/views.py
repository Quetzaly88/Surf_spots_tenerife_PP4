#import modules and classes
from django.shortcuts import render, redirect #renders HTML templates, redirects to a different URL
from .forms import RegistrationForm # Custom form class for user registration. 
from django.contrib import messages # displays messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
    #register view
def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid(): #check if form is valid, then save data to create user
            form.save()
            messages.success(request, 'Your account was successfully created!') #account created, redirect to login
            return redirect('login')
    else:
        form = RegistrationForm() #if GET render empty form
        
    return render(request, 'users_account/register.html', {'form': form}) #render the registration template and pass the form instance to the template context. 

    #login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")#form
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request)
            messages.success(request, "You are loged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'users_account/login.html')