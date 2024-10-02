from rest_framework import permissions, viewsets

from apps.kitten_api import serializers as kitten_api_serializers
from apps.kitten_api import models as kitten_api_models
from apps.kitten_api import filters as kitten_api_filters


class KittenViewSet(viewsets.ModelViewSet):
    model = kitten_api_models.Kitten
    serializer_class = kitten_api_serializers.KittenSerializer
    filterset_class = kitten_api_filters.KittenFilterSet

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action in ["retrieve", "list"]:
            return kitten_api_models.Kitten.objects.all()
        # Only owners can interact with their cats
        return kitten_api_models.Kitten.objects.filter(owner=self.request.user)


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    model = kitten_api_models.Breed
    serializer_class = kitten_api_serializers.BreedSerializer
    queryset = kitten_api_models.Breed.objects.all()
