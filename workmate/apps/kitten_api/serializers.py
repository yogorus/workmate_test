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
        fields = ["name", "age", "breed", "color", "owner", "id"]
        read_only_fields = (
            "owner",
            "id",
        )


class OutputKittenSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()

    class Meta:
        model = kitten_api_models.Kitten
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = kitten_api_models.Review
        fields = ["author", "kitten", "rating", "id"]
        read_only_fields = (
            "author",
            "id",
        )

    def validate(self, data):
        user = self.context["request"].user

        # Check if the author is not the owner of the kitten
        if data["kitten"].owner == user:
            raise ValidationError("You cannot rate your own kitten.")

        # Check if this user already has a review for the same kitten
        if kitten_api_models.Review.objects.filter(
            author=user, kitten=data["kitten"]
        ).exists():
            raise serializers.ValidationError("You have already reviewed this kitten.")

        return super().validate(data)


class OuputReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = kitten_api_models.Review
        fields = "__all__"
