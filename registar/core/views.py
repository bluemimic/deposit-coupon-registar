from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CouponForm

from groups.models import Group

from django.utils.translation import gettext_lazy as _

from .models import Shop, Coupon


class IndexView(TemplateView):
    """
    A view that renders the index page.
    """
    template_name = 'core/index.html'


# ========== Shop views ==========


class ShopListView(LoginRequiredMixin, ListView):
    """
    A view that renders a list of shops.
    """
    model = Shop
    context_object_name = "shops"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user.pk)


class ShopDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders a list of coupons for a shop.
    """
    model = Shop
    context_object_name = "shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk or shop.groups.filter(members=self.request.user.pk).exists()
    

class ShopCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view that creates a shop.
    """
    model = Shop
    fields = ['title', 'is_pinned']
    success_message = _("Shop created successfully")

    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class ShopUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a shop.
    """
    model = Shop
    fields = ['title', 'is_pinned']
    success_message = _("Shop updated successfully")

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    
class ShopDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a shop.
    """
    model = Shop
    success_url = '/shops/'
    success_message = _("Shop deleted successfully")

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk
    

# ========== Coupon views ==========
 

class CouponListView(LoginRequiredMixin, ListView):
    """
    A view that renders a list of shops.
    """
    model = Coupon
    context_object_name = "coupons"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user.pk)


class CouponDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders a list of coupons for a shop.
    """
    model = Coupon
    context_object_name = "coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk or coupon.store.groups.filter(members=self.request.user.pk).exists()


class CouponCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view that creates a coupon.
    """
    model = Coupon
    form_class = CouponForm
    success_message = _("Coupon created successfully")

    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CouponUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    A view that updates a coupon.
    """
    model = Coupon
    form_class = CouponForm
    success_message = _("Coupon updated successfully")

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


class CouponDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    A view that deletes a coupon.
    """
    model = Coupon
    success_url = '/coupons/'
    success_message = _("Coupon deleted successfully")

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk
