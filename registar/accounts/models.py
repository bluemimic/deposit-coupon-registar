from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model for the application.
    
    """
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ["-date_joined", "username"]
        verbose_name = _('user')
        verbose_name_plural = _('users')