from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from calculator.models import Pet, Food


class IndexView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        pet = Pet.objects.filter(owner=current_user.id, is_default=True).first()

        if not pet:
            pet = Pet.objects.filter(owner=current_user.id).first()

        return render(request, "calculator/index.html", {
            "current_user": current_user,
            "pet": pet,
        })


class PetCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        pet_name = request.POST.get("pet_name")
        is_default = request.POST.get("is_default") == "on"

        if is_default:
            Pet.objects.filter(owner=user, is_default=True).update(
                is_default=False)

        new_pet = Pet.objects.create(name=pet_name, owner=user, is_default=is_default)

        return redirect("calculator:pet_detail", pet_id=new_pet.id)

class PetDetailView(View):
    def get(self, request, pet_id, *args, **kwargs):
        current_user = request.user
        pet = Pet.objects.get(id=pet_id)
        return render(request, "calculator/pet_detail.html", {"current_user": current_user, "pet": pet})


class FoodCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pet_id = request.POST.get("pet_id")
        pet = Pet.objects.get(id=pet_id)

        food_name = request.POST.get("food_name")
        kcal = 1000
        meals = 3
        meal_size = 13

        pet.foods.create(
            name=food_name,
            kcal=kcal,
            meals=meals,
            meal_size=meal_size
        )

        messages.success(request, "Food created successfully!")
        return redirect("calculator:pet_detail", pet_id=pet.id)

class FoodDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pet_id = request.POST.get("pet_id")
        food_id = request.POST.get("food_id")

        food = Food.objects.get(id=food_id)
        food.delete()

        return redirect("calculator:pet_detail", pet_id=pet_id)