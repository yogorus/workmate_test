from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Breed(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"


class Kitten(models.Model):
    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=50, blank=False)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    breed = models.ForeignKey("kitten_api.Breed", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name} - {self.owner.username}"
