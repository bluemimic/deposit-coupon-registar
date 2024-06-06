from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("overview/", views.OverviewView.as_view(), name="overview"),

    path("shops/", views.ShopListView.as_view(), name="shop_list"),
    path("shops/<uuid:pk>/", views.ShopDetailView.as_view(), name="shop_detail"),
    path("shops/create/", views.ShopCreateView.as_view(), name="shop_create"),
    path("shops/<uuid:pk>/update/", views.ShopUpdateView.as_view(), name="shop_update"),
    path("shops/<uuid:pk>/delete/", views.ShopDeleteView.as_view(), name="shop_delete"),
    path("shops/<uuid:pk>/pin/", views.ShopPinView.as_view(), name="shop_pin"),
    path("shops/<uuid:pk>/unpin/", views.ShopUnpinView.as_view(), name="shop_unpin"),
    path("shops/<uuid:pk>/upload_to_marketplace/", views.ShopUploadToMarketplaceView.as_view(), name="shop_upload_to_marketplace"),
    path("shops/<uuid:pk>/remove_from_marketplace/", views.ShopRemoveFromMarketplaceView.as_view(), name="shop_remove_from_marketplace"),

    path("coupons/", views.CouponListView.as_view(), name="coupon_list"),
    path("coupons/<uuid:pk>/", views.CouponDetailView.as_view(), name="coupon_detail"),
    path("coupons/create/", views.CouponCreateView.as_view(), name="coupon_create"),
    path("coupons/<uuid:pk>/update/", views.CouponUpdateView.as_view(), name="coupon_update"),
    path("coupons/<uuid:pk>/delete/", views.CouponDeleteView.as_view(), name="coupon_delete"),
    path("coupons/<uuid:pk>/pin/", views.CouponPinView.as_view(), name="coupon_pin"),
    path("coupons/<uuid:pk>/unpin/", views.CouponUnpinView.as_view(), name="coupon_unpin"),
    
    path("coupons/<uuid:pk>/share/", views.CouponShareView.as_view(), name="coupon_share"),
    path("coupons/<uuid:pk>/unshare/", views.CouponUnshareView.as_view(), name="coupon_unshare"),
    path("coupons/shared/<uuid:pk>/", views.CouponSharedDetailView.as_view(), name="coupon_shared_detail"),
    path("coupons/<uuid:pk>/use/", views.CouponUseView.as_view(), name="coupon_use"),
    path("coupons/<uuid:pk>/unuse/", views.CouponUnuseView.as_view(), name="coupon_unuse"),
]
