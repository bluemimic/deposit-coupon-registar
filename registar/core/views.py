import logging
from itertools import chain
from typing import Any

import requests
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Case, Count, IntegerField, Q, Sum, Value, When
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
from groups.models import Group, GroupMembership

import registar.settings as settings

from .forms import CouponForm
from .models import Coupon, Shop

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """
    A view that renders the index page.
    """
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["shops"] = self.get_shops()
        context["coupons"] = self.get_coupons()
        context["groups"] = self.get_groups()

        amount_of_coupons = Sum('amount',  default=0)
        context["total_amount_returned"] = Coupon.objects.filter(owner=self.request.user.pk, is_used=True).aggregate(amount_of_coupons)['amount__sum']

        context["recent_coupons"] = Coupon.objects.filter(owner=self.request.user.pk).order_by('-date_added')[:3]
        context["pinned_coupons"] = Coupon.objects.filter(owner=self.request.user.pk, is_pinned=True)[:3]

        return context

    def get_shops(self):
        max_shops_in_index = settings.MAX_SHOPS_IN_INDEX

        count_of_unused_coupons = Sum(1, default = 0, filter = Q(coupon__is_used = False))
        count_of_coupons = Sum(1, default = 0)
        amount_of_unused_coupons = Sum(
                    'coupon__amount',
                    default=0,
                    filter=Q(
                        coupon__is_used=False
                    )
                )

        all_shops = Shop.objects.filter(
            owner=self.request.user.pk,
        ).annotate(
            amount_unused=amount_of_unused_coupons, 
            count_unused=count_of_unused_coupons, 
            count=count_of_coupons
        ).order_by(
            "-date_added"
        )

        pinned_shops = all_shops.filter(is_pinned=True)[:3]
        number_of_remaining_shops = max_shops_in_index - pinned_shops.count()
        unpinned_shops = all_shops.filter(is_pinned=False)[:number_of_remaining_shops]

        return list(chain(pinned_shops, unpinned_shops))
    
    def get_coupons(self):
        max_coupons_in_index = settings.MAX_COUPONS_IN_INDEX

        all_coupons = Coupon.objects.filter(
            owner=self.request.user.pk,
            is_used=False
        ).order_by(
            "-date_added"
        )

        pinned_coupons = all_coupons.filter(is_pinned=True)[:3]
        number_of_remaining_coupons = max_coupons_in_index - pinned_coupons.count()
        unpinned_coupons = all_coupons.filter(is_pinned=False)[:number_of_remaining_coupons]

        return list(chain(pinned_coupons, unpinned_coupons))

    def get_groups(self):
        
        # owned_groups = Group.objects.raw(
        #     f"""
        #     SELECT
        #         g.id,
        #         g.title,
        #         g.is_pinned,
        #         g.date_added,
        #         COUNT(DISTINCT m.user_id) AS member_count,
        #         COUNT(DISTINCT s.id) AS shop_count,
        #         COALESCE(SUM(CASE WHEN c.is_used = False THEN c.amount ELSE NULL END), 0) as money_amount
        #     FROM
        #         groups_group g
        #     LEFT JOIN
        #         groups_groupmembership m
        #     ON
        #         g.id = m.group_id
        #     LEFT JOIN
        #         groups_shopgroup s
        #     ON
        #         g.id = s.group_id
        #     LEFT JOIN
        #         core_shop sh
        #     ON
        #         s.shop_id = sh.id
        #     LEFT JOIN
        #         core_coupon c
        #     ON
        #         sh.id = c.store_id
        #     WHERE
        #         g.owner_id = {self.request.user.pk}
        #     GROUP BY
        #         g.id
        #     ORDER BY
        #         g.is_pinned DESC,
        #         g.date_added DESC
        #     """
        # )

        owned_groups = Group.objects.filter(owner_id=self.request.user.pk).annotate(
                member_count=Count('groupmembership__user_id', distinct=True),
                shop_count=Count('shopgroup__id', distinct=True),
                money_amount=Coalesce(Sum(
                    Case(
                        When(shops__coupon__is_used=False, then='shops__coupon__amount'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ), 0)
            ).order_by('-is_pinned', '-date_added')

        return owned_groups[:6]


class OverviewView(LoginRequiredMixin, TemplateView):
    """
    A view that renders the overview page.
    """
    template_name = 'core/overview.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        amount_of_coupons = Sum('amount',  default=0)
        
        total_amount = Coupon.objects.filter(owner=self.request.user.pk).aggregate(Sum('amount')).get('amount__sum', 0)
        context["total_amount"] = total_amount
        
        total_amount_returned = Coupon.objects.filter(owner=self.request.user.pk, is_used=True).aggregate(amount_of_coupons).get('amount__sum', 0)
        context["total_amount_returned"] = total_amount_returned
        
        total_amount_remaining = total_amount - total_amount_returned
        context["total_amount_remaining"] = total_amount_remaining

        context["returned_percentage"] = round(total_amount_returned / total_amount * 100, 2) if total_amount else 0

        context["total_shops"] = Shop.objects.filter(owner=self.request.user.pk).count()
        context["total_shops_pinned"] = Shop.objects.filter(owner=self.request.user.pk, is_pinned=True).count()
    
        context["total_coupons"] = Coupon.objects.filter(owner=self.request.user.pk).count()
        context["total_shared_coupons"] = Coupon.objects.filter(owner=self.request.user.pk, is_shared=True).count()
        context["total_pinned_coupons"] = Coupon.objects.filter(owner=self.request.user.pk, is_pinned=True).count()
        context["total_used_coupons"] = Coupon.objects.filter(owner=self.request.user.pk, is_used=True).count()
        context["total_unused_coupons"] = Coupon.objects.filter(owner=self.request.user.pk, is_used=False).count()
        
        context["used_percentage"] = round(context["total_used_coupons"] / context["total_coupons"] * 100, 2) if context["total_coupons"] else 0

        context["total_groups"] = Group.objects.filter(owner=self.request.user.pk).count()
        context["total_memberships"] = GroupMembership.objects.filter(group__owner=self.request.user.pk).count()

        return context


# ========== Shop views ==========


class ShopListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    A view that renders a list of shops.
    """
    model = Shop
    context_object_name = "shops"
    permission_required = "core.view_shop"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        amount_of_unused_coupons = Sum(
                    'coupon__amount',
                    default=0,
                    filter=Q(
                        coupon__is_used=False
                    )
                )

        count_of_unused_coupons = Sum(1, default = 0, filter = Q(coupon__is_used = False))
        count_of_coupons = Sum(1, default = 0)

        return queryset.filter(owner=self.request.user.pk).annotate(
            amount_unused=amount_of_unused_coupons, 
            count_unused=count_of_unused_coupons, 
            count=count_of_coupons
        ).order_by(
            "-is_pinned",
            "-date_added"
        )


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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        shop = self.get_object()

        context["coupons"] = shop.coupon_set.filter(owner=self.request.user.pk).order_by('-is_pinned', '-date_added')
        
        return context


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
        
        logger.info("User %s (pk: %d) created a shop %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    form.instance.title,
                    form.instance.pk
        )
        return super().form_valid(form)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the shop create view", request.user, request.user.pk)
        return super().get(request, *args, **kwargs)


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
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the shop update view for shop %s (pk: %s)",
                    request.user, request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) updated shop %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().form_valid(form)


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
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the shop delete view for shop %s (pk: %s)",
                    request.user, request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) deleted shop %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().form_valid(form)


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

        logger.info("User %s (pk: %d) pinned shop %s (pk: %s)",
                    request.user, request.user.pk,
                    shop.title,
                    shop.pk
        )
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
        
        logger.info("User %s (pk: %d) unpinned shop %s (pk: %s)",
                    request.user, request.user.pk,
                    shop.title,
                    shop.pk
        )
        return redirect('core:shop_detail', pk=shop.pk)

    def get_object(self, queryset=None):
        return Shop.objects.get(pk=self.kwargs['pk'])


class ShopUploadToMarketplaceView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that uploads a shop to the marketplace.
    """
    success_message = _("Shop uploaded to the marketplace successfully!")
    permission_required = "core.upload_to_marketplace_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        is_owner = shop.owner.pk == self.request.user.pk
        
        return is_owner and not shop.is_on_marketplace

    def post(self, request, *args, **kwargs):
        shop = self.get_object()
        shop.is_on_marketplace = True
        shop.save()

        messages.success(request, self.success_message)
        
        logger.info("User %s (pk: %d) uploaded shop %s (pk: %s) to the marketplace",
                    request.user, request.user.pk,
                    shop.title,
                    shop.pk
        )
        return redirect('core:shop_detail', pk=shop.pk)

    def get_object(self, queryset=None):
        return Shop.objects.get(pk=self.kwargs['pk'])
    

class ShopRemoveFromMarketplaceView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View):
    """
    A view that removes a shop from the marketplace.
    """
    success_message = _("Shop removed from the marketplace successfully!")
    permission_required = "core.remove_from_marketplace_shop"

    def test_func(self) -> bool:
        shop = self.get_object()
        is_owner = shop.owner.pk == self.request.user.pk
        
        return is_owner and shop.is_on_marketplace

    def post(self, request, *args, **kwargs):
        shop = self.get_object()
        shop.is_on_marketplace = False
        shop.save()

        messages.success(request, self.success_message)
        
        logger.info("User %s (pk: %d) removed shop %s (pk: %s) from the marketplace",
                    request.user, request.user.pk,
                    shop.title,
                    shop.pk
        )
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
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            owner=self.request.user.pk
        ).order_by(
            "-is_pinned",
            "is_used",
            "-date_added"
        )


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

        # Get the exchange rate
        url = "https://api.frankfurter.app/latest"
        params = {
            'amount': coupon.amount,
            'from': 'EUR',
            'to': 'USD'
        }

        response = requests.get(url, params=params)
        data = response.json()

        context["in_usd"] = round(data['rates']['USD'], 2)

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
        
        if not form.instance.title:
            form.instance.title = f"Unnamed coupon for shop {form.instance.store.title} ({form.instance.amount}€)"
        
        logger.info("User %s (pk: %d) created a coupon %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    form.instance.title,
                    form.instance.pk
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the coupon create view", request.user, request.user.pk)
        return super().get(request, *args, **kwargs)


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

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the coupon update view for coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        if not form.instance.title:
            form.instance.title = f"Unnamed coupon for shop {form.instance.store.title} ({form.instance.amount}€)"
        
        logger.info("User %s (pk: %d) created a coupon %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    form.instance.title,
                    form.instance.pk
        )

        logger.info("User %s (pk: %d) updated coupon %s (pk: %s)",
                    self.request.user, self.request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().form_valid(form)


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
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the coupon delete view for coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form: BaseForm) -> HttpResponse:
        logger.info("User %s (pk: %d) deleted coupon %s (pk: %s)",
                    self.request.user,
                    self.request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().form_valid(form)


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
        
        logger.info("User %s (pk: %d) shared coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
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
        
        logger.info("User %s (pk: %d) unshared coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        logger.info("User %s (pk: %d) requested the shared coupon detail view for coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    self.get_object().title,
                    self.get_object().pk
        )
        return super().get(request, *args, **kwargs)


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
        
        logger.info("User %s (pk: %d) marked coupon %s (pk: %s) as used",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
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
        
        logger.info("User %s (pk: %d) marked coupon %s (pk: %s) as unused",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
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
        
        logger.info("User %s (pk: %d) pinned coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
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
        
        logger.info("User %s (pk: %d) unpinned coupon %s (pk: %s)",
                    request.user, request.user.pk,
                    coupon.title,
                    coupon.pk
        )
        return redirect('core:coupon_detail', pk=coupon.pk)

    def get_object(self, queryset=None):
        return Coupon.objects.get(pk=self.kwargs['pk'])
