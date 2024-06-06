from rest_framework import permissions


class IsMemberOrOwnerShop(permissions.BasePermission):
    """
    Custom permission to only allow members of a group or the owner to view it.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_member = obj.groups.filter(members=request.user.pk).exists()

        return is_owner or is_member


class IsMemberOrOwnerCoupon(permissions.BasePermission):
    """
    Custom permission to only allow members of a group or the owner to view it.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_member = obj.store.groups.filter(members=request.user.pk).exists()

        return is_owner or is_member


class IsMemberOrOwnerGroup(permissions.BasePermission):
    """
    Custom permission to only allow members of a group or the owner to view it.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_member = obj.members.all().filter(pk=request.user.pk).exists()

        return is_owner or is_member


class IsRequestUser(permissions.BasePermission):
    """
    Custom permission to only allow the request user to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsSenderOrRecipient(permissions.BasePermission):
    """
    Custom permission to only allow the sender or recipient to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.recipient == request.user


class IsOnMarketplace(permissions.BasePermission):
    """
    Custom permission to only allow the request user to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_on_marketplace
