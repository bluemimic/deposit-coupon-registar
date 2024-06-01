from django.urls import path

from .views import (GroupPinView, GroupUnpinView, GroupAddShopView,
                    GroupCreateView, GroupDeleteView, GroupDetailView,
                    GroupInviteView, GroupRemoveMemberView,
                    GroupRemoveShopView, GroupsListView, GroupUpdateView,
                    InvitationAcceptView, InvitationDeclineView,
                    InvitationDetailView, InvitationsListView)

app_name = "groups"

urlpatterns = [
    path('', GroupsListView.as_view(), name='group_list'),
    path('<uuid:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path("create/", GroupCreateView.as_view(), name="group_create"),
    path("<uuid:pk>/update/", GroupUpdateView.as_view(), name="group_update"),
    path("<uuid:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    path("<uuid:pk>/pin/", GroupPinView.as_view(), name="group_pin"),
    path("<uuid:pk>/unpin/", GroupUnpinView.as_view(), name="group_unpin"),
    
    path("<uuid:pk>/invite/", GroupInviteView.as_view(), name="group_invite"),
    path("<uuid:pk>/remove/", GroupRemoveMemberView.as_view(), name="group_remove_member"),
    
    path("<uuid:pk>/add_shop/", GroupAddShopView.as_view(), name="group_add_shop"),
    path("<uuid:pk>/remove_shop/", GroupRemoveShopView.as_view(), name="group_remove_shop"),
    
    path("invitations/", InvitationsListView.as_view(), name="invitation_list"),
    path("invitations/<int:pk>/", InvitationDetailView.as_view(), name="invitation_detail"),
    path("invitations/<int:pk>/accept/", InvitationAcceptView.as_view(), name="invitation_accept"),
    path("invitations/<int:pk>/reject/", InvitationDeclineView.as_view(), name="invitation_reject"),
]
