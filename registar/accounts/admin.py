from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User
from core.models import Shop


@admin.action(description=_("Promote selected users to staff"))
def promote_to_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)
    
    
@admin.action(description=_("Demote selected users from staff"))
def demote_from_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)
    
    
@admin.action(description=_("Activate selected users"))
def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
    
    
@admin.action(description=_("Deactivate selected users"))
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


class ShopInline(admin.TabularInline):
    model = Shop


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User admin.
    """
    exclude = ["date_joined", "date_modified"]
    inlines = [ShopInline]
    list_display = ["username", "email", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_active"]
    save_as = True
    search_fields = ["first_name", "last_name", "email", "username"]
    search_help_text = _("Search by first name, last name, email, username")
    actions = [promote_to_staff, demote_from_staff, activate, deactivate]
