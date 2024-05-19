from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model for the application.
    
    """
    
    date_modified = models.DateTimeField(auto_now=True)
