from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "weight_unit", "password1", "password2"]


class UpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "currency", "weight_unit"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        queryset = (
            get_user_model().objects
            .filter(email=email)
            .exclude(pk=self.instance.pk)
        )
        if queryset.exists():
            raise forms.ValidationError("This email is already taken.")
        return email

