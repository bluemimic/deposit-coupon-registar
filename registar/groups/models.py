from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

import uuid


class Group(models.Model):
    """
    Group model.
    """
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_('group uuid'))
    title           = models.CharField(max_length=100, verbose_name=_('group title'))
    is_pinned       = models.BooleanField(default=False, verbose_name=_('is group pinned?'))
    owner           = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('owner of the group'))
    access_password = models.CharField(max_length=128, verbose_name=_('access password'), help_text=_("optional"), null=True, blank=True)
    members         = models.ManyToManyField(get_user_model(), verbose_name=_('members'), related_name='memberships', through='GroupMembership')
    shops           = models.ManyToManyField('core.Shop', verbose_name=_('shops'), related_name='groups', through='ShopGroup')
    date_added      = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    date_modified   = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ["-date_added", "title"]
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        
        permissions = [
            ("invite_user_group", _("Can invite user to a group")),
            ("remove_user_group", _("Can remove user from a group")),
            ("add_shop_group", _("Can add shop to a group")),
            ("remove_shop_group", _("Can remove shop from a group")),
        ]


    def get_absolute_url(self):
        return reverse('groups:group_detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.title


class GroupMembership(models.Model):
    """
    Group membership model.
    """
    user        = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'))
    group       = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    is_pinned   = models.BooleanField(default=False, verbose_name=_('is group pinned?'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('joined at'))
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_group_membership'),
        ]
        verbose_name = _('group membership')
        verbose_name_plural = _('group memberships')
        
    def __str__(self) -> str:
        return f"{ self.user.username } in { self.group.title }"


class ShopGroup(models.Model):
    """
    Shop group model for shared shops.
    """
    shop        = models.ForeignKey('core.Shop', on_delete=models.CASCADE, verbose_name=_('shop'))
    group       = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    is_pinned   = models.BooleanField(default=False, verbose_name=_('is shop pinned?'))
    date_added  = models.DateTimeField(auto_now_add=True, verbose_name=_('added at'))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shop', 'group'], name='unique_shop_group'),
        ]
        verbose_name = _('shop group')
        verbose_name_plural = _('shop groups')
 
    def __str__(self) -> str:
        return f"{ self.shop.title } in { self.group.title }"


class Invitation(models.Model):
    """
    Invitation model.
    """
    group           = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    sender          = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('sender'))
    recipient       = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('recipient'), related_name='invitations')
    is_accepted     = models.BooleanField(default=False, verbose_name=_('is accepted?'))
    is_processed    = models.BooleanField(default=False, verbose_name=_('is processed?'))
    date_sent       = models.DateTimeField(auto_now_add=True, verbose_name=_('sent at'))
    date_accepted   = models.DateTimeField(null=True, blank=True, verbose_name=_('accepted at'))
    date_rejected   = models.DateTimeField(null=True, blank=True, verbose_name=_('rejected at'))
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'recipient'], name='unique_invitation'),
        ]
        verbose_name = _('invitation')
        verbose_name_plural = _('invitations')
        
        permissions = [
            ("accept_invitation", _("Can accept invitation")),
            ("reject_invitation", _("Can reject invitation")),
        ]

    def __str__(self) -> str:
        return f"{ self.sender.username } invited { self.recipient.username } to { self.group.title }"

    def accept(self):
        self.group.members.add(self.recipient)
        self.date_accepted = timezone.now()
        self.date_rejected = None
        self.is_accepted = True
        self.is_processed = True
        self.save()

    def reject(self):
        self.group.members.remove(self.recipient)
        self.date_rejected = timezone.now()
        self.date_accepted = None
        self.is_accepted = False
        self.is_processed = True
        self.save()
