from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("pet/create/", views.PetCreateView.as_view(), name="pet_create"),
    path("pet/<int:pk>/", views.PetDetailView.as_view(), name="pet_detail"),
    path("pet/<int:pk>/update/", views.PetUpdateView.as_view(), name="pet_update"),
    path("pet/<int:pk>/delete/", views.PetDeleteView.as_view(), name="pet_delete"),
    path("pet/<int:pk>/calculate_price/", views.PetCalculatePrice.as_view(), name="calculate_price"),
    path("food/create/", views.FoodCreateView.as_view(), name="food_create"),
    path("food/<int:pk>/update/", views.FoodUpdateView.as_view(), name="food_update"),
    path("food/<int:pk>/delete/", views.FoodDeleteView.as_view(), name="food_delete"),
]
