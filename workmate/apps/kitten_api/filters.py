from django_filters import rest_framework as filters

from apps.kitten_api import models as kitten_api_models


class KittenFilterSet(filters.FilterSet):
    breed = filters.ModelChoiceFilter(queryset=kitten_api_models.Breed.objects.all())

    class Meta:
        model = kitten_api_models.Kitten
        fields = ["breed"]
