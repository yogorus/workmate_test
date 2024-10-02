from rest_framework import serializers

from apps.kitten_api import models as kitten_api_models


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = kitten_api_models.Breed
        fields = "__all__"


class KittenSerializer(serializers.ModelSerializer):

    class Meta:
        model = kitten_api_models.Kitten
        fields = "__all__"
