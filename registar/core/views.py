from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
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


class ShopPinView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that pins a shop.
    """
    success_message = _("Shop pinned successfully!")
    permission_required = "core.change_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk and not shop.is_pinned

    def post(self, request, *args, **kwargs):
        shop = self.get_object()
        shop.is_pinned = True
        shop.save()

        messages.success(request, self.success_message)
        return redirect('core:shop_detail', pk=shop.pk)

    def get_object(self, queryset=None):
        return Shop.objects.get(pk=self.kwargs['pk'])
    

class ShopUnpinView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that unpins a shop.
    """
    success_message = _("Shop unpinned successfully!")
    permission_required = "core.change_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        return shop.owner.pk == self.request.user.pk and shop.is_pinned

    def post(self, request, *args, **kwargs):
        shop = self.get_object()
        shop.is_pinned = False
        shop.save()

        messages.success(request, self.success_message)
        return redirect('core:shop_detail', pk=shop.pk)

    def get_object(self, queryset=None):
        return Shop.objects.get(pk=self.kwargs['pk'])

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        coupon = self.get_object()

        shared_url = self.request.build_absolute_uri(reverse('core:coupon_shared_detail', kwargs={'pk': coupon.pk}))
        context["shared_url"] = shared_url

        return context


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


class CouponShareView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that shares a coupon.
    """
    success_message = _("Coupon shared successfully! Access URL: %(url)s")
    permission_required = "core.share_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and not coupon.is_shared

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_shared = True
        coupon.save()

        messages.success(request, self.get_success_message(cleaned_data=None))
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])

    def get_success_message(self, cleaned_data):
        coupon = self.get_object()
        shared_url = self.request.build_absolute_uri(reverse('core:coupon_shared_detail', kwargs={'pk': coupon.pk}))
        return self.success_message % {'url': shared_url}


class CouponUnshareView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that unshares a coupon.
    """
    success_message = _("Coupon unshared successfully!")
    permission_required = "core.unshare_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and coupon.is_shared

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_shared = False
        coupon.save()
        
        messages.success(request, self.success_message)
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])


class CouponSharedDetailView(DetailView):
    """
    A view that renders a shared coupon.
    """
    model = Coupon
    context_object_name = "coupon"
    template_name = 'core/coupon_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Coupon, pk=self.kwargs['pk'], is_shared=True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        coupon = self.get_object()

        shared_url = self.request.build_absolute_uri(reverse('core:coupon_shared_detail', kwargs={'pk': coupon.pk}))
        context["shared_url"] = shared_url

        return context


class CouponUseView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that marks a coupon as used.
    """
    success_message = _("Coupon marked as used successfully!")
    permission_required = "core.change_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and not coupon.is_used

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_used = True
        coupon.save()

        messages.success(request, self.success_message)
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])


class CouponUnuseView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that marks a coupon as unused.
    """
    success_message = _("Coupon marked as unused successfully!")
    permission_required = "core.change_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and coupon.is_used

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_used = False
        coupon.save()

        messages.success(request, self.success_message)
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])


class CouponPinView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that pins a coupon.
    """
    success_message = _("Coupon pinned successfully!")
    permission_required = "core.change_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and not coupon.is_pinned

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_pinned = True
        coupon.save()

        messages.success(request, self.success_message)
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])


class CouponUnpinView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that unpins a coupon.
    """
    success_message = _("Coupon unpinned successfully!")
    permission_required = "core.change_coupon"

    def test_func(self) -> bool:
        coupon = self.get_object()
        return coupon.owner.pk == self.request.user.pk and coupon.is_pinned

    def post(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.is_pinned = False
        coupon.save()

        messages.success(request, self.success_message)
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])
