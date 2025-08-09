from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DetailView, CreateView

from calculator.models import Pet, Food


class IndexView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        pet = Pet.objects.filter(owner=current_user.id, is_default=True).first()

        if not pet:
            pet = Pet.objects.filter(owner=current_user.id).first()

        return render(
            request,
            "calculator/index.html",
            {
                "current_user": current_user,
                "pet": pet,
            },
        )


class PetCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        pet_name = request.POST.get("pet_name")
        is_default = request.POST.get("is_default") == "on"

        if is_default:
            Pet.objects.filter(owner=user, is_default=True).update(is_default=False)

        new_pet = Pet.objects.create(name=pet_name, owner=user, is_default=is_default)

        return redirect("calculator:pet_detail", pk=new_pet.id)


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = "calculator/pet_detail.html"
    context_object_name = "pet"

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    fields = ["name", "is_default"]
    template_name = "calculator/pet_update.html"

    def form_valid(self, form):
        is_default = form.cleaned_data.get("is_default")
        if is_default:
            Pet.objects.filter(owner=self.request.user, is_default=True).update(is_default=False)
        messages.success(self.request, "Pet updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("calculator:pet_detail", kwargs={"pk": self.object.id})


class FoodCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pet_id = request.POST.get("pet_id")
        pet = get_object_or_404(Pet, pk=pet_id)

        food_name = request.POST.get("food_name", "name")
        kcal = request.POST.get("kcal", 0)
        meals = request.POST.get("meals", 0)
        meal_size = request.POST.get("meal_size", 0)

        package_size = request.POST.get("package_size", 0)
        package_price = request.POST.get("package_price", 0.00)

        pet.foods.create(
            name=food_name,
            kcal=kcal,
            meals=meals,
            meal_size=meal_size,
            package_size=package_size,
            package_price=package_price
        )

        return redirect("calculator:pet_detail", pk=pet.id)


class FoodUpdateView(LoginRequiredMixin, View):
    def post(self, request, food_id, *args, **kwargs):
        food = get_object_or_404(Food, pk=food_id)

        # Update fields
        food.name = request.POST.get("food_name", food.name)
        food.kcal = int(request.POST.get("kcal") or food.kcal or 0)
        food.meals = int(request.POST.get("meals") or food.meals or 0)
        food.meal_size = int(request.POST.get("meal_size") or food.meal_size or 0)
        food.package_size = int(request.POST.get("package_size") or food.package_size or 0)
        food.package_price = float(request.POST.get("package_price") or food.package_price or 0)
        food.save()

        # htmx request → re-render single card
        if request.headers.get("Hx-Request") == "true":
            return render(request, "includes/food_card.html", {
                "food": food,
                "pet": food.pet
            })

        return redirect("calculator:pet_detail", pk=food.pet.id)



class FoodDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pet_id = request.POST.get("pet_id")
        food_id = request.POST.get("food_id")

        food = get_object_or_404(Food, pk=food_id)
        food.delete()

        return redirect("calculator:pet_detail", pk=pet_id)
