from django.urls import path

from .views import (
    UserDetailView,
    UserSettingsView, UserDeleteView,
)

app_name = "users"

urlpatterns = [
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("me/settings/", UserSettingsView.as_view(), name="user-settings"),
    path("me/delete/", UserDeleteView.as_view(), name="user-delete"),
]
