from django.urls import path
from calculator import views

app_name = "calculator"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pet/create/", views.PetCreateView.as_view(), name="pet_create"),
    path("pet/<int:pet_id>/", views.PetDetailView.as_view(), name="pet_detail"),
    path("food/create/", views.FoodCreateView.as_view(), name="food_create"),
    path("food/delete/", views.FoodDeleteView.as_view(), name="food_delete"),

]
