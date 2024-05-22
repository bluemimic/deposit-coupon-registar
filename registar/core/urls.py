from django.urls import path
from .views import (IndexView, ShopDetailView, ShopListView, CouponDetailView, CouponListView, ShopCreateView, ShopUpdateView, 
                    ShopDeleteView, CouponCreateView, CouponUpdateView, CouponDeleteView)

from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("shops/", ShopListView.as_view(), name="shop_list"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shop_detail"),
    path("shops/create/", ShopCreateView.as_view(), name="shop_create"),
    path("shops/<int:pk>/update/", ShopUpdateView.as_view(), name="shop_update"),
    path("shops/<int:pk>/delete/", ShopDeleteView.as_view(), name="shop_delete"),

    path("coupons/", CouponListView.as_view(), name="coupon_list"),
    path("coupons/<int:pk>/", CouponDetailView.as_view(), name="coupon_detail"),
    path("coupons/create/", CouponCreateView.as_view(), name="coupon_create"),
    path("coupons/<int:pk>/update/", CouponUpdateView.as_view(), name="coupon_update"),
    path("coupons/<int:pk>/delete/", CouponDeleteView.as_view(), name="coupon_delete"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
