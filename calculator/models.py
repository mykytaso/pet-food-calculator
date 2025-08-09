from django.db import models

from users.models import User


class Pet(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    is_default = models.BooleanField(default=False)
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
    name = models.CharField(max_length=100, blank=True, null=True)
    kcal = models.PositiveIntegerField(default=0)
    meals = models.PositiveIntegerField(default=0)
    meal_size = models.PositiveIntegerField(default=0)

    package_size = models.PositiveIntegerField(default=0)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="foods")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def kcal_per_day(self):
        return round((self.kcal / 1000) * self.meal_size * self.meals, 2)

    @property
    def cost_per_day(self):
        if self.package_size > 0 and self.package_price > 0:
            return round(
                (self.package_price / self.package_size) * self.meal_size * self.meals,
                2,
            )
        return 0.00
