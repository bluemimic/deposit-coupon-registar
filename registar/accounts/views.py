import logging
from typing import Any

import django.contrib.auth.views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, TemplateView,
                                  UpdateView)

from .forms import UserRegisterForm

logger = logging.getLogger(__name__)


class CustomLoginView(SuccessMessageMixin, auth_views.LoginView):
    """
    View for logging in a user.
    """
    def form_valid(self, form):       
        logger.info("User %s (pk: %d) logged in", form.get_user(), form.get_user().pk)
        return super().form_valid(form)


class CustomLogoutView(SuccessMessageMixin, auth_views.LogoutView):
    """
    View for logging out a user.
    """
    def post(self, request, *args, **kwargs):
        logger.info("User %s (pk: %d) logged out", request.user, request.user.pk)
        return super().post(request, *args, **kwargs)
    

class CustomPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    """
    View for changing a user's password.
    """
    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) changed their password", self.request.user, self.request.user.pk)
        return super().form_valid(form)


class SignUpView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    """
    View for registering a new user.
    """
    template_name = 'registration/register.html'
    success_url = reverse_lazy('account:login')
    form_class = UserRegisterForm
    success_message = _("Your profile was created successfully")

    def test_func(self):
        return not self.request.user.is_authenticated

    def form_valid(self, form: BaseForm) -> HttpResponse:
        form_valid = super().form_valid(form)
        logger.info("User %s (pk: %d) registered", form.instance.username, form.instance.pk)
        return form_valid


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    View for displaying a user's profile.
    """
    template_name = 'registration/profile.html'
    permission_required = "accounts.view_user"


class ContactAdminView(LoginRequiredMixin, TemplateView):
    """
    View for contacting the admin in case of forgotten password.
    Temporary solution for MVP.
    """
    template_name = 'registration/contact_admin.html'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a user.
    """
    model = get_user_model()
    fields = ['username', 'first_name', 'last_name', 'email']
    success_message = _("User updated successfully")
    template_name = 'registration/user_form.html'
    permission_required = "accounts.change_user"

    def test_func(self) -> bool:
        user = self.get_object()
        return user.pk == self.request.user.pk

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) updated their profile", form.instance, form.instance.pk)
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a user.
    """
    model = get_user_model()
    success_url = reverse_lazy('core:index')
    success_message = _("User deleted successfully")
    template_name = 'registration/user_confirm_delete.html'
    permission_required = "accounts.delete_user"

    def test_func(self) -> bool:
        user = self.get_object()
        return user.pk == self.request.user.pk

    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) deleted their profile", self.get_object(), self.get_object().pk)
        return super().form_valid(form)
