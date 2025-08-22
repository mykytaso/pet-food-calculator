import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from calculator.helpers import tm_new_user_created


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

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

    weight_unit = models.CharField(
        max_length=2, choices=UNIT_CHOICES, default="g"
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="$")
    has_visited_buy_me_coffee = models.BooleanField(default=False)


@receiver(post_save, sender=get_user_model())
def new_user_created_telegram_notification(sender, instance, created, **kwargs):
    if created:
        tm_new_user_created(instance.date_joined, instance.email)
