from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from .views import ContactAdminView, ProfileView, SignUpView, UserUpdateView, UserDeleteView


from . import views as custom_auth


app_name = "account"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("profile/<int:pk>/update/", UserUpdateView.as_view(), name="profile_update"),
    path("profile/<int:pk>/delete/", UserDeleteView.as_view(), name="profile_delete"),

    path("password_change/", custom_auth.CustomPasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("contact_admin/", ContactAdminView.as_view(), name="contact_admin"),

    path("login/", custom_auth.CustomLoginView.as_view(), name="login"),
    path("logout/", custom_auth.CustomLogoutView.as_view(), name="logout"),

    path("", include("django.contrib.auth.urls")),
] 
