import uuid
from decimal import Decimal

from django.db import models

from users.models import User


class Pet(models.Model):
    CALCULATE_PRICE_CHOICES = [
        ("on", "On"),
        ("off", "Off"),
    ]

    PET_ICON_CHOICES = [
        ("cat_icon.png", "Cat"),
        ("dog_icon.png", "Dog"),
        # ("bird", "Bird"),
        # ("hamster", "Hamster"),
        # ("rabbit", "Rabbit"),
        # ("turtle", "Turtle"),
        # ("snake", "Snake"),
        # ("lizard", "Lizard"),
        # ("frog", "Frog"),
        # ("hedgehog", "Hedgehog"),
        # ("guinea_pig", "Guinea Pig"),
        # ("chinchilla", "Chinchilla"),
        ("other_icon.png", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    is_default = models.BooleanField(default=False)
    calculate_price = models.CharField(max_length=3, choices=CALCULATE_PRICE_CHOICES, default="off")
    pet_icon = models.CharField(max_length=30, choices=PET_ICON_CHOICES, default="other_icon.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_pet_per_owner"
            )
        ]
        ordering = ["created_at"]


class Food(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    kcal = models.PositiveIntegerField(blank=True, null=True)
    meals = models.PositiveIntegerField(blank=True, null=True)
    meal_size = models.PositiveIntegerField(blank=True, null=True)

    package_size = models.PositiveIntegerField(blank=True, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="foods")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    @property
    def kcal_per_day(self):
        if None in (self.kcal, self.meals, self.meal_size):
            return 0
        if 0 in (self.kcal, self.meals, self.meal_size):
            return 0

        return round((self.kcal / 1000) * self.meal_size * self.meals, 2)


    @property
    def cost_per_day(self):
        if None in (self.kcal, self.meals, self.meal_size, self.package_size, self.package_price):
            return Decimal(0.00)
        if 0 in (self.kcal, self.meals, self.meal_size, self.package_size, self.package_price):
            return Decimal(0.00)

        return round(
            (self.package_price / self.package_size) * self.meal_size * self.meals,
            2,
        )
