from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    UNIT_CHOICES = [("g", "Grams"), ("lb", "Pounds")]

    username = None
    email = models.EmailField(unique=True)

    weight_unit = models.CharField(
        max_length=2, choices=UNIT_CHOICES, default="g"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
