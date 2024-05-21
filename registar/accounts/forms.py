from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user.
    """
    email = forms.EmailField(label=_("Email"), required=True)

    class Meta:
        """
        Metadata for the UserRegisterForm class.
        """
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
