from django.urls import path

from .views import (
    UserRegisterView,
    UserDetailView,
    UserUpdateView,
    UserPasswordChangeView,
    UserLoginView,
    UserLogoutView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("me/update/", UserUpdateView.as_view(), name="user-update"),
    path(
        "me/password_change/",
        UserPasswordChangeView.as_view(),
        name="password-change",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
