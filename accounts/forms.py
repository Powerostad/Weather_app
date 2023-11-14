from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "country",
            "city",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "country",
            "city",
        )
