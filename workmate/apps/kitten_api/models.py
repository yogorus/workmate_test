from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.


class Breed(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True, null=True)


class Kitten(models.Model):
    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=50, blank=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    breed = models.ForeignKey("kitten_api.Breed", on_delete=models.CASCADE)
