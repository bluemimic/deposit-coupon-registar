from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm

class SignUpView(SuccessMessageMixin, CreateView):
    """
    View for registering a new user.
    """
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View for displaying a user's profile.
    """
    template_name = 'registration/profile.html'
    

class ContactAdminView(TemplateView):
    """
    View for contacting the admin in case of forgotten password.
    Temporary solution for MVP.
    """
    template_name = 'registration/contact_admin.html'
