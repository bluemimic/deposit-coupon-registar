from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib import admin


class Shop(models.Model):
    """
    Shop model.
    """
    title           = models.CharField(max_length=100, verbose_name=_('shop title'))
    is_pinned       = models.BooleanField(default=False, verbose_name=_('is shop pinned?'))
    owner           = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('owner of the shop'))
    date_added      = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    date_modified   = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ["-date_added", "title"]
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def __str__(self) -> str:
        return self.title


class Coupon(models.Model):
    """
    Coupon model.
    """
    title            = models.CharField(max_length=100, verbose_name=_('coupon title'), help_text=_("can be null"), null=True, blank=True)
    barcode          = models.CharField(max_length=200, verbose_name=_('coupon barcode'))
    is_used          = models.BooleanField(default=False, verbose_name=_('is used?'))
    is_pinned        = models.BooleanField(default=False, verbose_name=_('is pinned?'))
    is_shared        = models.BooleanField(default=False, verbose_name=_('is shared?'))
    amount           = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('amount'))
    store            = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('store'))
    date_added       = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    date_modified    = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ["-date_added", "title"]
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')

    def __str__(self) -> str:
        return self.title
