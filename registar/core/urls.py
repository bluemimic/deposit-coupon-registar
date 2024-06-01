from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (CouponCreateView, CouponDeleteView, CouponDetailView,
                    CouponListView, CouponShareView, CouponUnshareView,
                    CouponUnuseView, CouponUpdateView, CouponUseView,
                    IndexView, ShopCreateView, ShopDeleteView, ShopDetailView,
                    ShopListView, ShopUpdateView, CouponSharedDetailView,
                    ShopPinView, ShopUnpinView, CouponPinView, CouponUnpinView)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("shops/", ShopListView.as_view(), name="shop_list"),
    path("shops/<uuid:pk>/", ShopDetailView.as_view(), name="shop_detail"),
    path("shops/create/", ShopCreateView.as_view(), name="shop_create"),
    path("shops/<uuid:pk>/update/", ShopUpdateView.as_view(), name="shop_update"),
    path("shops/<uuid:pk>/delete/", ShopDeleteView.as_view(), name="shop_delete"),
    path("shops/<uuid:pk>/pin/", ShopPinView.as_view(), name="shop_pin"),
    path("shops/<uuid:pk>/unpin/", ShopUnpinView.as_view(), name="shop_unpin"),

    path("coupons/", CouponListView.as_view(), name="coupon_list"),
    path("coupons/<uuid:pk>/", CouponDetailView.as_view(), name="coupon_detail"),
    path("coupons/create/", CouponCreateView.as_view(), name="coupon_create"),
    path("coupons/<uuid:pk>/update/", CouponUpdateView.as_view(), name="coupon_update"),
    path("coupons/<uuid:pk>/delete/", CouponDeleteView.as_view(), name="coupon_delete"),
    path("coupons/<uuid:pk>/pin/", CouponPinView.as_view(), name="coupon_pin"),
    path("coupons/<uuid:pk>/unpin/", CouponUnpinView.as_view(), name="coupon_unpin"),
    
    path("coupons/<uuid:pk>/share/", CouponShareView.as_view(), name="coupon_share"),
    path("coupons/<uuid:pk>/unshare/", CouponUnshareView.as_view(), name="coupon_unshare"),
    path("coupons/shared/<uuid:pk>/", CouponSharedDetailView.as_view(), name="coupon_shared_detail"),
    path("coupons/<uuid:pk>/use/", CouponUseView.as_view(), name="coupon_use"),
    path("coupons/<uuid:pk>/unuse/", CouponUnuseView.as_view(), name="coupon_unuse"),
]

