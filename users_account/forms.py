# import statements
from django import forms  # used to create user input
from django.contrib.auth.forms import UserCreationForm  # build in for user registration
from .models import NovaUser  # imports the custom NovaUSer
from .models import SurfSpot

# define RegistrationForm class.
# adds email to the form, ensures valid email, uses widget appearance.


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter your email'
        })
    )

# nested class with the form that provides metadata about the form. Meta allowws to automatically populate fields.
    class Meta:
        model = NovaUser
        fields = ['username', 'email', 'password1', 'password2']


# used save Method
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SurfSpotForm(forms.ModelForm):
    class Meta:
        model = SurfSpot
        fields = ['title', 'location', 'description', 'best_seasons']