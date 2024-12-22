#import modules and classes
from django.shortcuts import render, redirect #renders HTML templates, redirects to a different URL
from .forms import RegistrationForm # Custom form class for user registration. 
from django.contrib import messages # displays messages

# Create your views here.
def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form_valid(): #check if form is valid, then save data to create user
            form.save()
            messages.success(request, 'Your account was successfully created!') #account created, redirect to login
            return redirect('login')
    else:
        form = RegistrationForm() #if GET render empty form
        
return render(request, 'users_account/register.html', {'form': form}) #render the registration template and pass the form instance to the template context. 


