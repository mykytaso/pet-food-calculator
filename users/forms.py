from django import forms
from django.contrib.auth import get_user_model


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "currency",
        ]


class MessageForm(forms.Form):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Your email (optional)"}),
    )
    message = forms.CharField(label="Message", max_length=1000, widget=forms.Textarea)


from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    """Custom login form to remove 'Forgot your password?'."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields["password"].help_text = None
