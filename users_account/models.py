# used build in django AbstractUser for pre-defined fields. 
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# custom user model = NovaUser

class NovaUser(AbstractUser):
    pass #add custom fields if needed. 