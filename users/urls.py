from django.urls import path

from .views import (
    UserDetailView,
    UserSettingsView,
)

app_name = "users"

urlpatterns = [
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("me/settings/", UserSettingsView.as_view(), name="user-settings"),
]
