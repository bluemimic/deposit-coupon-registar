from core.models import Coupon, Shop
from django.contrib.auth import get_user_model
from django.db.models import Q
from groups.models import Group, Invitation
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .permissions import (IsMemberOrOwnerCoupon, IsMemberOrOwnerGroup,
                          IsMemberOrOwnerShop, IsOnMarketplace, IsRequestUser,
                          IsSenderOrRecipient)
from .serializers import (CouponSerializer, GroupSerializer,
                          InvitationSerializer, MarketplaceSerializer,
                          ShopSerializer, UserSerializer)

User = get_user_model()


class Index(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': reverse('api:user_detail', args=[request.user.pk], request=request, format=format),
            'shops': reverse('api:shop_list', request=request, format=format),
            'coupons': reverse('api:coupon_list', request=request, format=format),
            'groups': reverse('api:group_list', request=request, format=format),
            'invitations': reverse('api:invitation_list', request=request, format=format),
            'marketplace': reverse('api:marketplace_list', request=request, format=format),
        }
        return Response(content)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsRequestUser]


class ShopList(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(Q(owner=self.request.user.pk) | Q(groups__members=self.request.user.pk)).distinct()


class ShopDetail(generics.RetrieveAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberOrOwnerShop]

    def get_queryset(self):
        return Shop.objects.all()


class CouponList(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Coupon.objects.filter(Q(owner=self.request.user.pk) | Q(store__groups__members=self.request.user.pk)).distinct()


class CouponDetail(generics.RetrieveAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberOrOwnerCoupon]

    def get_queryset(self):
        return Coupon.objects.all()


class GroupList(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(Q(owner=self.request.user.pk) | Q(members=self.request.user.pk)).distinct()


class GroupDetail(generics.RetrieveAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberOrOwnerGroup]

    def get_queryset(self):
        return Group.objects.all()


class InvitationList(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Invitation.objects.filter(Q(sender=self.request.user.pk) | Q(recipient=self.request.user.pk)).distinct()


class InvitationDetail(generics.RetrieveAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrRecipient]

    def get_queryset(self):
        return Invitation.objects.all()


class MarketplaceList(generics.ListAPIView):
    serializer_class = MarketplaceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOnMarketplace]

    def get_queryset(self):
        return Shop.objects.filter(is_on_marketplace=True)
