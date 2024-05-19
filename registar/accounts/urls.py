from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from .views import ProfileView, SignUpView

app_name = "account"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password_change/", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("", include("django.contrib.auth.urls")),
]