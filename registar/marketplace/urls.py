from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path('', views.ShopListView.as_view(), name='shop_list'),
    path('shop/<uuid:pk>/', views.ShopDetailView.as_view(), name='shop_detail'),
    path('shop/<uuid:pk>/use/', views.ShopUseView.as_view(), name='shop_use'),
]