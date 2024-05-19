from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user.
    """
    email = forms.EmailField()

    class Meta:
        """
        Metadata for the UserRegisterForm class.
        """
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
