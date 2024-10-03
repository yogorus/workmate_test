from django.db import models
from django.db.models import Avg
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
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="kittens"
    )
    breed = models.ForeignKey("kitten_api.Breed", on_delete=models.CASCADE)

    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def rating(self):
        average_rating = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        return round(average_rating, 1) if average_rating is not None else 0

    def __str__(self) -> str:
        return f"{self.pk} - {self.name} - {self.owner.username}"


class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reviews"
    )
    kitten = models.ForeignKey(
        "kitten_api.Kitten", related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.author} - {self.kitten.pk} - {self.kitten.name}: {self.rating}"
