from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

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

