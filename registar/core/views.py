from typing import Any

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from groups.models import Group

from .forms import CouponForm
from .models import Coupon, Shop


class IndexView(TemplateView):
    """
    A view that renders the index page.
    """
    template_name = 'core/index.html'


# ========== Shop views ==========


class ShopListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    A view that renders a list of shops.
    """
    model = Shop
    context_object_name = "shops"
    permission_required = "core.view_shop"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user.pk)


class ShopDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders a list of coupons for a shop.
    """
    model = Shop
    context_object_name = "shop"
    permission_required = "core.view_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk or shop.groups.filter(members=self.request.user.pk).exists()
    

class ShopCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view that creates a shop.
    """
    model = Shop
    fields = ['title', 'is_pinned']
    success_message = _("Shop created successfully")
    permission_required = "core.add_shop"

    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class ShopUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a shop.
    """
    model = Shop
    fields = ['title', 'is_pinned']
    success_message = _("Shop updated successfully")
    permission_required = "core.change_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    
class ShopDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a shop.
    """
    model = Shop
    success_url = '/shops/'
    success_message = _("Shop deleted successfully")
    permission_required = "core.delete_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk
    

# ========== Coupon views ==========
 

class CouponListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    A view that renders a list of shops.
    """
    model = Coupon
    context_object_name = "coupons"
    permission_required = "core.view_coupon"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user.pk)


class CouponDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders a list of coupons for a shop.
    """
    model = Coupon
    context_object_name = "coupon"
    permission_required = "core.view_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk or coupon.store.groups.filter(members=self.request.user.pk).exists()


class CouponCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view that creates a coupon.
    """
    model = Coupon
    form_class = CouponForm
    success_message = _("Coupon created successfully")
    permission_required = "core.add_coupon"

    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CouponUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a coupon.
    """
    model = Coupon
    form_class = CouponForm
    success_message = _("Coupon updated successfully")
    permission_required = "core.change_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CouponDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a coupon.
    """
    model = Coupon
    success_url = '/coupons/'
    success_message = _("Coupon deleted successfully")
    permission_required = "core.delete_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk
