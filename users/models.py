from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    UNIT_CHOICES = [("g", "Grams"), ("lb", "Pounds")]
    CURRENCY_CHOICES = [
        ("$", "US Dollar"),
        ("€", "Euro"),
        ("£", "British Pound"),
        ("¥", "Japanese Yen"),
        ("₴", "Ukrainian Hryvnia"),
        ("₹", "Indian Rupee"),
        ("₺", "Turkish Lira"),
        ("₩", "South Korean Won"),
        ("C$", "Canadian Dollar"),
        ("A$", "Australian Dollar"),
        ("CHF", "Swiss Franc"),
        ("NZ$", "New Zealand Dollar"),
        ("SEK", "Swedish Krona"),
        ("NOK", "Norwegian Krone"),
        ("DKK", "Danish Krone"),
        ("SGD", "Singapore Dollar"),
        ("HK$", "Hong Kong Dollar"),
        ("MX$", "Mexican Peso"),
        ("BRL", "Brazilian Real"),
    ]

    username = None
    email = models.EmailField(unique=True)

    weight_unit = models.CharField(
        max_length=2, choices=UNIT_CHOICES, default="g"
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="$")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
