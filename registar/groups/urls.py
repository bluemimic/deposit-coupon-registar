from django.urls import path

from .views import (
    GroupDeleteView, GroupUpdateView, GroupsListView, GroupDetailView, 
    GroupCreateView, GroupInviteView, InvitationsListView, InvitationDetailView,
    InvitationAcceptView, InvitationDeclineView, GroupRemoveMemberView, GroupAddShopView,
    GroupRemoveShopView
    )

app_name = "groups"

urlpatterns = [
    path('', GroupsListView.as_view(), name='group_list'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path("create/", GroupCreateView.as_view(), name="group_create"),
    path("<int:pk>/update/", GroupUpdateView.as_view(), name="group_update"),
    path("<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    
    path("<int:pk>/invite/", GroupInviteView.as_view(), name="group_invite"),
    path("<int:pk>/remove/", GroupRemoveMemberView.as_view(), name="group_remove_member"),
    
    path("<int:pk>/add_shop/", GroupAddShopView.as_view(), name="group_add_shop"),
    path("<int:pk>/remove_shop/", GroupRemoveShopView.as_view(), name="group_remove_shop"),
    
    path("invitations/", InvitationsListView.as_view(), name="invitation_list"),
    path("invitations/<int:pk>/", InvitationDetailView.as_view(), name="invitation_detail"),
    path("invitations/<int:pk>/accept/", InvitationAcceptView.as_view(), name="invitation_accept"),
    path("invitations/<int:pk>/reject/", InvitationDeclineView.as_view(), name="invitation_reject"),
]
