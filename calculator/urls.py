from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pet/create/", views.PetCreateView.as_view(), name="pet_create"),
    path("pet/<int:pk>/", views.PetDetailView.as_view(), name="pet_detail"),
    path("pet/<int:pk>/update/", views.PetUpdateView.as_view(), name="pet_update"),
    path("pet/<int:pk>/delete/", views.PetDeleteView.as_view(), name="pet_delete"),
    path("food/create/", views.FoodCreateView.as_view(), name="food_create"),
    path("food/<int:food_id>/update/", views.FoodUpdateView.as_view(), name="food_update"),
    path("food/<int:pk>/delete/", views.FoodDeleteView.as_view(), name="food_delete"),
]
