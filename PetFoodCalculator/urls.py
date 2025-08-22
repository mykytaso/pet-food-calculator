from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("", include("calculator.urls", namespace="calculator")),
] + debug_toolbar_urls()
