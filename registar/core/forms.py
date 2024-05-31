from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from numpy import frombuffer, uint8

from .models import Coupon, Shop
from .utils import extract_barcode, NoBarcodeData, NoBarcodeDetected


class CouponForm(forms.ModelForm):
    """
    A form that creates a coupon.
    """
    coupon_image = forms.ImageField(required=False, label=_("Coupon image"))
    barcode = forms.CharField(required=False, label=_("Barcode"), widget=forms.TextInput(attrs={'placeholder': _("Barcode")}))

    class Meta:
        model = Coupon
        fields = ['title', 'barcode', 'is_used', 'is_pinned', 'amount', 'store']
        localized_fields = '__all__'
        field_order = ['title', 'barcode', 'coupon_image', 'is_used', 'is_pinned', 'amount', 'store']


    def __init__(self, *args, **kwargs):
        """
        This __init__ method is used to filter the store field based on the user.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.order_fields(self.Meta.field_order)
        self.fields['store'].queryset = Shop.objects.filter(owner=self.user.pk)


    def clean_store(self):
        store = self.cleaned_data["store"]
        if store.owner.pk != self.user.pk:
            raise ValidationError(_("You cannot select another user's store!"))

        return store


    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('coupon_image') and cleaned_data.get('barcode'):
            raise ValidationError(_("You cannot provide both a barcode and an image to a coupon!"))

        if not cleaned_data.get('coupon_image') and not cleaned_data.get('barcode'):
            raise ValidationError(_("You must provide either a barcode or an image to a coupon!"))

        if cleaned_data.get('barcode'):
            return cleaned_data

        coupon_image = self.cleaned_data.get("coupon_image")
        numpy_image = frombuffer(coupon_image.read(), uint8)

        try:
            barcode = extract_barcode(numpy_image)

        except NoBarcodeDetected:
            raise ValidationError(_("No barcode detected in the image."))

        except NoBarcodeData:
            raise ValidationError(_("No data found in the barcode."))

        self.cleaned_data["barcode"] = barcode

        return cleaned_data
