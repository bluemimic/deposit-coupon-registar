from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    
    path("user/<int:pk>/", views.UserDetail.as_view(), name="user_detail"),

    path("shops/", views.ShopList.as_view(), name="shop_list"),
    path("shops/<uuid:pk>/", views.ShopDetail.as_view(), name="shop_detail"),

    path("coupons/", views.CouponList.as_view(), name="coupon_list"),
    path("coupons/<uuid:pk>/", views.CouponDetail.as_view(), name="coupon_detail"),
    
    path("groups/", views.GroupList.as_view(), name="group_list"),
    path("groups/<uuid:pk>/", views.GroupDetail.as_view(), name="group_detail"),

    path("invitations/", views.InvitationList.as_view(), name="invitation_list"),
    path("invitations/<int:pk>/", views.InvitationDetail.as_view(), name="invitation_detail"),
    
    path("marketplace/", views.MarketplaceList.as_view(), name="marketplace_list"),
]
