from django.forms import ModelForm, PasswordInput, CheckboxSelectMultiple, Form
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


from core.models import Shop

from .models import Group, Invitation


class GroupForm(ModelForm):
    """
    A form that creates a coupon.
    """
    class Meta:
        model = Group
        fields = ['title', 'is_pinned', 'access_password']
        localized_fields = '__all__'

        widgets = {
            'access_password': PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        This __init__ method is used to filter the shops field based on the user.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_access_password(self):
        access_password = self.cleaned_data["access_password"]
        if access_password:
            access_password = make_password(access_password)

        return access_password


class AddShopForm(Form):
    """
    A form that adds a shop to a group.
    """

    shop = forms.ModelChoiceField(queryset=None, label=_("shop"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

    def clean_shop(self):
        shop = self.cleaned_data["shop"]

        if shop.owner.pk != self.user.pk:
            raise ValidationError(_("You cannot select another user's shop!"))

        if self.group.shops.filter(pk=shop.pk).exists():
            raise ValidationError(_("Shop is already added to the group!"))

        return shop
    
class RemoveShopForm(AddShopForm):
    """
    A form that removes a shop from a group.
    """
    
    def clean_shop(self):
        shop = self.cleaned_data["shop"]
        
        if shop.owner.pk != self.user.pk:
            raise ValidationError(_("You cannot select another user's shop!"))

        if not self.group.shops.filter(pk=shop.pk).exists():
            raise ValidationError(_("Shop is not added to the group!"))

        return shop


class InvitationForm(Form):
    """
    A form that invites a user to a group.
    """

    username = forms.CharField(label=_("username"), max_length=150)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not get_user_model().objects.filter(username=username).exists():
            raise ValidationError(_("User does not exist!"))

        if get_user_model().objects.filter(username=username).first() == self.user:
            raise ValidationError(_("You cannot invite yourself!"))

        if self.group.members.filter(username=username).exists():
            raise ValidationError(_("User is already a member of the group!"))
        
        if Invitation.objects.filter(group=self.group, recipient__username=username).exists():
            raise ValidationError(_("Invitation has already been sent to this user!"))

        return username


class RemoveMemberForm(Form):
    """
    A form that removes a member from a group.
    """

    user = forms.ModelChoiceField(queryset=None, label=_("user"))

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

    def clean_user(self):
        user = self.cleaned_data["user"]

        if user == self.group.owner.pk:
            raise ValidationError(_("You cannot remove the owner of the group!"))

        if not self.group.members.filter(pk=user.pk).exists():
            raise ValidationError(_("User is not a member of the group!"))

        return user


class InvitationAcceptForm(Form):
    """
    A form that accepts an invitation.
    """

    access_password = forms.CharField(label=_("access password"), max_length=128, widget=PasswordInput())
