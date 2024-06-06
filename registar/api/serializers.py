from core.models import Coupon, Shop
from django.contrib.auth import get_user_model
from groups.models import Group, Invitation
from rest_framework import permissions, serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']


class ShopSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'title', 'groups', 'is_pinned', 'is_on_marketplace', 'owner', 'date_added', 'date_modified']
        permisions = [permissions.IsAuthenticated]


class CouponSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = Coupon
        fields = ['id', 'title', 'barcode', 'is_used', 'is_pinned', 'is_shared', 'amount', 'store', 'owner', 'date_added', 'date_modified']


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    invitations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'title', 'is_pinned', 'owner', 'members', 'invitations', 'access_password', 'shops', 'date_added', 'date_modified']


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'group', 'sender', 'recipient', 'is_accepted', 'is_processed', 'date_sent', 'date_accepted', 'date_rejected']
        permisions = [permissions.IsAuthenticated]


class MarketplaceSerializer(ShopSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'title', 'owner', 'date_added', 'date_modified']
        permisions = [permissions.IsAuthenticated]
