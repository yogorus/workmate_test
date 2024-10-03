from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.kitten_api import models as kitten_api_models


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = kitten_api_models.Breed
        fields = "__all__"


class KittenSerializer(serializers.ModelSerializer):

    class Meta:
        model = kitten_api_models.Kitten
        fields = ["name", "age", "breed", "color", "owner"]
        read_only_fields = ("owner",)


class UpdateKittenSerializer(serializers.ModelSerializer):

    class Meta:
        model = kitten_api_models.Kitten
        fields = ["name", "age", "breed", "color"]


class OutputKittenSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()

    class Meta:
        model = kitten_api_models.Kitten
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = kitten_api_models.Review
        fields = ["author", "kitten", "rating"]
        read_only_fields = ("author",)

    def validate(self, data):
        # Check if the author is not the owner of the kitten
        if data["kitten"].owner == self.context["request"].user:
            raise ValidationError("You cannot rate your own kitten.")
        return super().validate(data)


class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = kitten_api_models.Review
        fields = ["rating"]


class OuputReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = kitten_api_models.Review
        fields = "__all__"
