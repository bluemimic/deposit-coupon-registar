from typing import Any
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from django.utils.translation import gettext_lazy as _

from .forms import UserRegisterForm

class SignUpView(SuccessMessageMixin, CreateView):
    """
    View for registering a new user.
    """
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:login')
    form_class = UserRegisterForm
    success_message = _("Your profile was created successfully")


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


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a user.
    """
    model = get_user_model()
    fields = ['username', 'first_name', 'last_name', 'email']
    success_message = _("User updated successfully")
    template_name = 'registration/user_form.html'

    def test_func(self) -> bool:
        user = self.get_object()
        return user.pk == self.request.user.pk

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a user.
    """
    model = get_user_model()
    success_url = reverse_lazy('core:index')
    success_message = _("User deleted successfully")
    template_name = 'registration/user_confirm_delete.html'

    def test_func(self) -> bool:
        user = self.get_object()
        return user.pk == self.request.user.pk
