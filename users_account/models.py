# used build in django AbstractUser for pre-defined fields. 
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class NovaUser(AbstractUser):
    pass #custom fields if needed. 