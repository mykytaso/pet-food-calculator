from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DetailView, DeleteView

from calculator.models import Pet, Food


class IndexView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user

        if not current_user.is_authenticated:
            return render(request, "calculator/home_guest.html")

        pets = Pet.objects.filter(owner=current_user)
        pet = (
            pets.filter(is_default=True).first() or pets.order_by("created_at").first()
        )
        if pet:
            return redirect("calculator:pet_detail", pk=pet.id)

        return render(request, "calculator/home.html")


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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("calculator:pet_detail", kwargs={"pk": self.object.id})


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    success_url = reverse_lazy("calculator:index")


class FoodCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pet_id = request.POST.get("pet_id")
        pet = get_object_or_404(Pet, pk=pet_id)
        new_food = Food.objects.create(pet=pet,)
        return render(request, "includes/food_form.html", {"food": new_food, "pet": pet})


class FoodUpdateView(LoginRequiredMixin, View):
    @staticmethod
    def to_int_or_none(n) -> int | None:
        try:
            return int(n)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def to_float_or_none(n) -> float | None:
        try:
            return float(n)
        except (ValueError, TypeError):
            return None

    def post(self, request, food_id, *args, **kwargs):
        food = get_object_or_404(Food, pk=food_id)

        food.name = request.POST.get("name") or None
        food.kcal = self.to_int_or_none(request.POST.get("kcal"))
        food.meals = self.to_int_or_none(request.POST.get("meals"))
        food.meal_size = self.to_int_or_none(request.POST.get("meal_size"))
        food.package_size = self.to_int_or_none(request.POST.get("package_size"))
        food.package_price = self.to_float_or_none(request.POST.get("package_price"))

        food.save()
        food.refresh_from_db()
        return render(request, "includes/food_form.html", {"food": food, "pet": food.pet})


class FoodDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        food_id = kwargs.get("pk")
        food = get_object_or_404(Food, pk=food_id)
        food.delete()
        return HttpResponse("")
