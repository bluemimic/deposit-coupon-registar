from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Shop, Coupon


@admin.action(description=_("Pin selected item"))
def pin(modeladmin, request, queryset):
    queryset.update(is_pinned=True)

@admin.action(description=_("Unpin selected item"))
def unpin(modeladmin, request, queryset):
    queryset.update(is_pinned=False)

@admin.action(description=_("Mark selected coupons as used"))
def use(modeladmin, request, queryset):
    queryset.update(is_used=True)

@admin.action(description=_("Mark selected coupons as unused"))
def unuse(modeladmin, request, queryset):
    queryset.update(is_used=False)
    
class CouponInline(admin.TabularInline):
    model = Coupon


class ShopAdmin(admin.ModelAdmin):
    """
    Shop admin.
    """
    actions = [pin, unpin]
    date_hierarchy = "date_added"
    exclude = ["date_added, date_modified"]
    list_display = ["title", "owner", "is_pinned", "date_added"]
    list_filter = ["owner", "is_pinned"]
    save_as = True
    search_fields = ["title", "owner__username", "owner__email"]
    search_help_text = _("Search by title, owner username, owner email")
    
    inlines = [CouponInline]
    

class CouponAdmin(admin.ModelAdmin):
    """
    Coupon admin.
    """
    actions = [pin, unpin, use, unuse]
    date_hierarchy = "date_added"
    exclude = ["date_added, date_modified"]
    list_display = ["title", "get_owner_username", "store", "amount", "is_pinned", "is_used", "date_added"]
    list_filter = ["is_pinned"]
    save_as = True
    search_fields = ["title", "barcode", "store__owner__username", "store__owner__email", "amount", "store__title"]
    search_help_text = _("Search by title, barcode, owner username, owner email, amount, store title")

    @admin.display(description=_("Owner's username"), ordering="store__owner__username")
    def get_owner_username(self, obj):
        return obj.store.owner.username


admin.site.register(Shop, ShopAdmin)
admin.site.register(Coupon, CouponAdmin)

