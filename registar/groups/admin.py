from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from .models import Group, Invitation


@admin.action(description=_("Pin selected item"))
def pin(modeladmin, request, queryset):
    queryset.update(is_pinned=True)

@admin.action(description=_("Unpin selected item"))
def unpin(modeladmin, request, queryset):
    queryset.update(is_pinned=False)

@admin.action(description=_("Accept invitation"))
def accept_invitation(modeladmin, request, queryset):
    for invitation in queryset:
        invitation.accept()

@admin.action(description=_("Reject invitation"))
def reject_invitation(modeladmin, request, queryset):
    for invitation in queryset:
        invitation.reject()


class GroupMembershipInline(admin.TabularInline):
    model = Group.members.through


class ShopGroupInline(admin.TabularInline):
    model = Group.shops.through


class GroupAdmin(admin.ModelAdmin):
    """
    Group admin.
    """
    actions = [pin, unpin]
    inlines = [GroupMembershipInline, ShopGroupInline]
    date_hierarchy = "date_added"
    exclude = ["date_added, date_modified"]
    list_display = ["title", "owner", "is_pinned", "get_members_count", "get_shop_count", "date_added"]
    list_filter = ["is_pinned"]
    save_as = True
    search_fields = ["title", "owner__username", "owner__email"]
    search_help_text = _("Search by title, barcode, owner username, owner email")

    @admin.display(description=_("Members"))
    def get_members_count(self, obj):
        return obj.members.count()

    @admin.display(description=_("Shops"))
    def get_shop_count(self, obj):
        return obj.shops.count()
    
    def save_model(self, request, obj, form, change):
        access_password = make_password(form.cleaned_data["access_password"])
        if access_password:
            obj.access_password = access_password
        super().save_model(request, obj, form, change)

    
class InvitationAdmin(admin.ModelAdmin):
    """
    Group admin.
    """
    actions = [accept_invitation, reject_invitation]
    date_hierarchy = "date_sent"
    exclude = ["date_accepted","date_rejected", "date_sent"]
    list_display = ["group", "sender", "recipient", "is_processed", "is_accepted", "date_sent", "date_accepted", "date_rejected"]
    save_as = True
    search_fields = ["group__title", "sender__username", "sender__email", "recipient__username", "recipient__email"]
    search_help_text = _("Search by group title, sender username, sender email, recipient username, recipient email")


admin.site.register(Group, GroupAdmin)
admin.site.register(Invitation, InvitationAdmin)
