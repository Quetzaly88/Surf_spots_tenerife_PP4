# used build in django AbstractUser for pre-defined fields.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# custom user model = NovaUser
class NovaUser(AbstractUser):
    pass

# Create your models here.
# import the models class from Django
from django.db import models

# creating a model class below. https://angelogentileiii.medium.com/basics-of-django-model-view-template-mvt-architecture-8585aecffbf6
#SurfSpot model representing surf spots
class SurfSpot(models.Model):
    CATEGORY_CHOICES = [
        ("Beginner", "Beginner"),
        ("Advanced", "Advanced"),
        ("For Everyone", "For Everyone"),
    ]

    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    best_seasons = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="For Everyone") # New category field
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#Comment model to represent comments on surf spots
class Comment(models.Model):
    surf_spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE, related_name="comments")#a foreign key to the Surf Spot linking to each comment. 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField() #content of the comment
    created_at = models.DateTimeField(auto_now_add=True) # timestamp when was the comment created

    def __str__(self): # returns string showing the first 20 characters of the comment
        #Display the comment (limited to 20 characters) and user. 
        return f"{self.content[:20]}... by {self.user.username}"
