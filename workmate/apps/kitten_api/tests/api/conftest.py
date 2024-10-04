import pytest

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from apps.kitten_api.models import Breed


@pytest.fixture
def create_breeds():
    """Fixture to create a few breed instances."""
    breed1 = Breed.objects.create(
        name="Siamese", description="A sleek, short-haired breed"
    )
    breed2 = Breed.objects.create(
        name="Persian", description="A long-haired, fluffy breed"
    )
    breed3 = Breed.objects.create(
        name="Maine Coon", description="A large, friendly breed"
    )

    return [breed1, breed2, breed3]


@pytest.fixture
def user_1():
    user = User.objects.create_user(
        username="foo", password="foopassword", email="foo@email.com"
    )
    refresh = RefreshToken.for_user(user)
    return user, str(refresh.access_token)


@pytest.fixture
def user_2():
    user = User.objects.create_user(
        username="bar", password="bar", email="bar@email.com"
    )
    refresh = RefreshToken.for_user(user)
    return user, str(refresh.access_token)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def client_user_1(user_1):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_1[1])
    return client


@pytest.fixture
def client_user_2(user_2):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_2[1])
    return client
