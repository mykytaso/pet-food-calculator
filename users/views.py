from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from PetFoodCalculator import settings
from calculator.helpers import (
    tm_user_visited_bmc_first_time,
    tm_user_visited_bmc_again,
    tm_guest_visited_bmc_first_time
)
from users.forms import UserSettingsForm


class UserDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/user_detail.html"


class UserSettingsView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserSettingsForm
    template_name = "users/user_settings.html"
    success_url = reverse_lazy("users:user-detail")

    def get_object(self, queryset=None):
        return self.request.user



class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("calculator:home")

    def get_object(self, queryset=None):
        return self.request.user


class BuyMeCoffeeView(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.has_visited_buy_me_coffee:
            request.user.has_visited_buy_me_coffee = True
            request.user.save(update_fields=["has_visited_buy_me_coffee"])
            tm_user_visited_bmc_first_time(request.user)
        elif request.user.is_authenticated and request.user.has_visited_buy_me_coffee:
            tm_user_visited_bmc_again(request.user)
        else:
            tm_guest_visited_bmc_first_time()
        return redirect(getattr(settings, "BUY_ME_A_COFFEE_LINK"))
