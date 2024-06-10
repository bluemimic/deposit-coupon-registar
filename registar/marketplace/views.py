import logging

from core.models import Shop
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View

logger = logging.getLogger(__name__)


class ShopListView(ListView):
    """
    A view that renders the list page of all shops.
    """
    model = Shop
    template_name = "marketplace/shop_list.html"
    context_object_name = "shops"

    def get_queryset(self):
        return Shop.objects.filter(is_on_marketplace=True)


class ShopDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders the detail page of a shop.
    """
    model = Shop
    template_name = "marketplace/shop_detail.html"
    context_object_name = "shop"
    permission_required = "marketplace.view_shop"

    def test_func(self):
        return self.get_object().is_on_marketplace


class ShopUseView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, View):
    """
    A view that adds a shop to the user's account.
    """
    permission_required = "groups.use_shop_from_marketplace"
    success_message = _("Shop '%(title)s' has been added to your account.")

    def test_func(self):
        return self.get_object().is_on_marketplace

    def post(self, request, pk):
        shop = self.get_object()

        new_shop = Shop.objects.create(
            title=shop.title,
            owner=request.user,
            is_on_marketplace=False,
        )

        messages.success(request, self.get_success_message())
         
        logger.info("User %s (pk: %d) added shop %s (pk: %s) to their account",
                    request.user, request.user.pk,
                    new_shop.title,
                    new_shop.pk
        )
        return redirect("core:shop_detail", pk=new_shop.pk)
    
    def get_success_message(self, cleaned_data=None) -> str:
        return self.success_message % {"title": self.get_object().title}

    def get_object(self, queryset=None):
        return get_object_or_404(Shop, pk=self.kwargs['pk'], is_on_marketplace=True)
