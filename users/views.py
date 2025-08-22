from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from PetFoodCalculator import settings
from calculator.helpers import (
    tm_user_visited_bmc_first_time,
    tm_user_visited_bmc_again,
    tm_guest_visited_bmc_first_time,
    tm_send_message,
)
from users.forms import UserSettingsForm, MessageForm


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
            tm_user_visited_bmc_first_time.delay(request.user.email)
        elif request.user.is_authenticated and request.user.has_visited_buy_me_coffee:
            tm_user_visited_bmc_again.delay(request.user.email)
        else:
            tm_guest_visited_bmc_first_time.delay()
        return redirect(getattr(settings, "BUY_ME_A_COFFEE_LINK"))


class SendMessageView(generic.View):
    def get(self, request, *args, **kwargs):
        form = MessageForm()
        return render(request, "users/send_message.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            tm_send_message.delay(
                message=form.cleaned_data.get("message", ""),
                email=form.cleaned_data.get("email", ""),
            )
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect("users:send-message")
        else:
            return redirect("users:send-message")
