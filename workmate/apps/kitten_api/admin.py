from django.contrib import admin
from apps.kitten_api import models as kitten_api_models


@admin.register(kitten_api_models.Kitten)
class KittenAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "breed", "age"]
    list_display_links = ["id"]
    list_filter = ["breed", "owner"]
    search_fields = ["name"]


@admin.register(kitten_api_models.Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    search_fields = ["name"]
