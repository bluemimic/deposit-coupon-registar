from typing import Any

from core.models import Shop
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from .forms import (AddShopForm, GroupForm, InvitationAcceptForm,
                    InvitationForm, RemoveMemberForm, RemoveShopForm)
from .models import Group, Invitation


class IndexView(TemplateView):
    """
    A view that renders the index page.
    """
    template_name = 'groups/index.html'


# ========== Group views ==========


class GroupsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    A view that renders a list of groups.
    """
    model = Group
    context_object_name = "groups"
    permission_required = "groups.view_group"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(Q(owner=self.request.user.pk) | Q(members=self.request.user.pk)).distinct()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['invitation_count'] = Invitation.objects.filter(recipient=self.request.user, is_processed=False).count()
        return context


class GroupDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders a list of coupons for a group.
    """
    model = Group
    context_object_name = "group"
    permission_required = "groups.view_group"

    def test_func(self) -> bool:
        group = self.get_object()
        return group.owner.pk == self.request.user.pk or group.members.filter(pk=self.request.user.pk).exists()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['shops'] = Invitation.objects.filter(recipient=self.request.user, is_processed=False).count()
        return context


class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view that creates a group.
    """
    model = Group
    form_class = GroupForm
    success_message = _("Group created successfully")
    permission_required = "groups.add_group"

    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a group.
    """
    model = Group
    form_class = GroupForm
    success_message = _("Group updated successfully")
    permission_required = "groups.change_group"

    def test_func(self) -> bool:
        group = self.get_object()
        return group.owner.pk == self.request.user.pk

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context


class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a group.
    """
    model = Group
    success_message = _("Group deleted successfully")
    success_url = reverse_lazy('groups:group_list')
    permission_required = "groups.delete_group"

    def test_func(self) -> bool:
        group = self.get_object()
        return group.owner.pk == self.request.user.pk


class GroupInviteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    A view that renders the group invitation page.
    """
    template_name = 'groups/invite.html'
    form_class = InvitationForm
    success_message = _("Invitation sent successfully")
    permission_required = "groups.invite_user_group"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return kwargs

    def test_func(self) -> bool:
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group.owner.pk == self.request.user.pk

    def get_success_url(self):
        return reverse_lazy('groups:group_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        try:
            user = get_user_model().objects.get(username=form.cleaned_data['username'])
            group = Group.objects.get(pk=self.kwargs['pk'])
     
            Invitation.objects.create(sender=self.request.user, recipient=user, group=group)

        except Group.DoesNotExist:
            return HttpResponse(status=404)

        return super().form_valid(form)


class GroupRemoveMemberView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    A view that removes a member from a group.
    """
    template_name = 'groups/remove_member.html'
    form_class = RemoveMemberForm
    success_message = _("Member removed successfully")
    permission_required = "groups.remove_user_group"

    def test_func(self) -> bool:
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group.owner.pk == self.request.user.pk

    def get_success_url(self):
        return reverse_lazy('groups:group_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['user'].queryset = get_object_or_404(Group, pk=self.kwargs['pk']).members.all()
        return form
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form: BaseForm):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        user = form.cleaned_data['user']
        group.members.remove(user)

        try:
            invitation = Invitation.objects.get(group=group, recipient=user)
            invitation.delete()
        except Invitation.DoesNotExist:
            pass

        return super().form_valid(form)


class GroupAddShopView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    A view that adds a shop to a group.
    """
    template_name = 'groups/add_shop.html'
    form_class = AddShopForm
    success_message = _("Shop added successfully")
    permission_required = "groups.add_shop_group"

    def test_func(self) -> bool:
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group.owner.pk == self.request.user.pk

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['shop'].queryset = Shop.objects.filter(owner=self.request.user).exclude(pk__in=get_object_or_404(Group, pk=self.kwargs['pk']).shops.all())
        return form

    def get_success_url(self):
        return reverse_lazy('groups:group_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        shop = form.cleaned_data['shop']
        is_pinned = form.cleaned_data['is_pinned']
        group.shops.add(shop, through_defaults={'is_pinned': is_pinned})
        return super().form_valid(form)


class GroupRemoveShopView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    A view that removes a shop from a group.
    """
    template_name = 'groups/remove_shop.html'
    form_class = RemoveShopForm
    success_message = _("Shop removed successfully")
    permission_required = "groups.remove_shop_group"

    def test_func(self) -> bool:
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group.owner.pk == self.request.user.pk

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['shop'].queryset = get_object_or_404(Group, pk=self.kwargs['pk']).shops.all()
        return form

    def get_success_url(self):
        return reverse_lazy('groups:group_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        shop = form.cleaned_data['shop']
        group.shops.remove(shop)
        return super().form_valid(form)


class InvitationsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    A view that renders a list of invitations.
    """
    model = Invitation
    context_object_name = "invitations"
    permission_required = "groups.view_invitation"

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user, is_processed=False).order_by('-date_sent')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['accepted'] = Invitation.objects.filter(recipient=self.request.user, is_accepted=True, is_processed=True)
        context['rejected'] = Invitation.objects.filter(recipient=self.request.user, is_accepted=False, is_processed=True)
        return context
   

class InvitationDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders the invitation detail page.
    """
    model = Invitation
    context_object_name = "invitation"
    permission_required = "groups.view_invitation"

    def test_func(self) -> bool:
        invitation = self.get_object()
        return invitation.recipient.pk == self.request.user.pk and not invitation.is_processed


class InvitationAcceptView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, View):
    """
    A view that accepts an invitation.
    """
    permission_required = "groups.accept_invitation"

    def test_func(self) -> bool:
        invitation = get_object_or_404(Invitation, pk=self.kwargs['pk'])
        return invitation.recipient.pk == self.request.user.pk and not invitation.is_processed

    def get_success_url(self):
        return reverse_lazy('groups:invitation_list')

    def get(self, request, *args, **kwargs):
        invitation = get_object_or_404(Invitation, pk=kwargs['pk'])
        group = invitation.group

        if not group.access_password:
            invitation.accept()
            messages.add_message(request, messages.INFO, _("Invitation accepted successfully"))
            return redirect('groups:invitation_list')
        else:
            return render(request, 'groups/accept.html', {'form': InvitationAcceptForm()})

    def post(self, request, *args, **kwargs):
        invitation = get_object_or_404(Invitation, pk=kwargs['pk'])
        group = invitation.group
        form = InvitationAcceptForm(request.POST)

        if form.is_valid():
            if check_password(form.cleaned_data['access_password'], group.access_password):
                invitation.accept()
                messages.add_message(request, messages.INFO, _("Invitation accepted successfully"))
                return redirect('groups:invitation_list')
            else:
                form.add_error('access_password', _("Access password is incorrect!"))

        return render(request, 'groups/accept.html', {'form': form})


class InvitationDeclineView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that declines an invitation.
    """
    success_message = _("Invitation declined successfully")
    permission_required = "groups.reject_invitation"

    def test_func(self) -> bool:
        invitation = get_object_or_404(Invitation, pk=self.kwargs['pk'])
        return invitation.recipient.pk == self.request.user.pk and not invitation.is_processed
    
    def get(self, request, *args, **kwargs):
        invitation = get_object_or_404(Invitation, pk=kwargs['pk'])
        invitation.reject()
        messages.add_message(request, messages.WARNING, _("Invitation was declined"))
        return redirect('groups:invitation_list')