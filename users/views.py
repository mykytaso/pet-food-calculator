from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View

from users.forms import RegisterForm, UpdateForm


class UserRegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:user-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/user_detail.html"


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UpdateForm
    template_name = "users/user_detail_update.html"
    success_url = reverse_lazy("users:user-detail")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:user-detail")

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("calculator:home")
