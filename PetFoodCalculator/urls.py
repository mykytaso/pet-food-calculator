from django.contrib import admin
from django.urls import path, include

from PetFoodCalculator import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("", include("calculator.urls", namespace="calculator")),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
