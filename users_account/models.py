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
class SurfSpot(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    best_seasons = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title