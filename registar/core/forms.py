from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Coupon, Shop


class CouponForm(ModelForm):
    """
    A form that creates a coupon.
    """
    class Meta:
        model = Coupon
        fields = ['title', 'barcode', 'is_used', 'is_pinned', 'amount', 'store']
        localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        This __init__ method is used to filter the store field based on the user.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['store'].queryset = Shop.objects.filter(owner=self.user.pk)

    def clean_store(self):
        store = self.cleaned_data["store"]
        if store.owner.pk != self.user.pk:
            raise ValidationError(_("You cannot select another user's store!"))

        return store