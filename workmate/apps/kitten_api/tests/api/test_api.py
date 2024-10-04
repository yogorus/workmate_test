import pytest


@pytest.mark.django_db
def test_create_without_token(client):
    response = client.post("/api/v1/kittens/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_kittens_are_empty(client):
    response = client.get("/api/v1/kittens/")
    assert len(response.data) == 0


@pytest.mark.django_db
def test_breeds_are_not_empty(client, create_breeds):
    response = client.get("/api/v1/breeds/")
    assert len(response.data) == 3


# @pytest.mark.django_db
@pytest.fixture
def test_kitten_creation(
    user_1,
    user_2,
    client_user_1,
    client_user_2,
    create_breeds,
):
    payload_1 = {
        "name": "Max",
        "age": 0,
        "breed": create_breeds[0].pk,
        "color": "black",
    }
    payload_2 = {
        "name": "Luna",
        "age": 5,
        "breed": create_breeds[1].pk,
        "color": "white",
    }

    # Test user 1 creation
    response_1 = client_user_1.post("/api/v1/kittens/", data=payload_1)

    assert response_1.status_code == 201
    assert response_1.data["name"] == payload_1["name"]
    assert response_1.data["owner"] == user_1[0].pk

    # Test user 2 creation
    response_2 = client_user_2.post("/api/v1/kittens/", data=payload_2)

    assert response_2.status_code == 201
    assert response_2.data["name"] == payload_2["name"]
    assert response_2.data["owner"] == user_2[0].pk

    # Test retrieve kitten
    response = client_user_1.get(f'/api/v1/kittens/{response_1.data['id']}/')
    assert response.data["name"] == payload_1["name"]
    assert response.data["owner"] == user_1[0].pk
    assert response.data['color'] == payload_1['color']
    assert response.data["breed"] == payload_1['breed']

    return (response_1.data, response_2.data)


@pytest.mark.django_db
def test_breed_filter(client, create_breeds, test_kitten_creation):
    response_1 = client.get(f"/api/v1/kittens/?breed={create_breeds[1].pk}")

    assert response_1.status_code == 200
    assert len(response_1.data) == 1
    assert response_1.data[0]["breed"] == create_breeds[1].pk

    response_2 = client.get(f"/api/v1/kittens/?breed={create_breeds[0].pk}")

    assert response_2.status_code == 200
    assert len(response_2.data) == 1
    assert response_2.data[0]["breed"] == create_breeds[0].pk

    response_3 = client.get(f"/api/v1/kittens/?breed={create_breeds[2].pk}")

    assert response_3.status_code == 200
    assert len(response_3.data) == 0


@pytest.mark.django_db
def test_crud_kitten(client_user_1, create_breeds, test_kitten_creation):
    # Test that user_1 can't redact user_2 kitten
    payload = {'name': "Bob"}

    put_payload = {'name': "Joe", "age": 0, "color": "red", "breed": create_breeds[2].pk}

    response_1 = client_user_1.patch(f"/api/v1/kittens/{test_kitten_creation[1]["id"]}/", payload)

    assert response_1.status_code == 404

    # Test PATCH

    response_2 = client_user_1.patch(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/", payload)

    assert response_2.status_code == 200
    assert response_2.data['name'] == payload["name"]

    # Test invalid data
    response_age = client_user_1.patch(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/", {"age": 13})
    assert response_age.status_code == 400

    response_color = client_user_1.patch(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/", {"color": 5})

    assert response_color.status_code == 400

    response_breed = client_user_1.patch(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/", {"breed": "Siamese"})
    assert response_breed.status_code == 400

    # Test PUT
    response_put = client_user_1.put(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/", put_payload)

    assert response_put.status_code == 200
    assert response_put.data['id'] == test_kitten_creation[0]["id"]
    assert response_put.data['name'] == put_payload['name']
    assert response_put.data['age'] == put_payload['age']
    assert response_put.data['color'] == put_payload['color']
    assert response_put.data['breed'] == put_payload['breed']

    # Test DELETE user_1 own kitten
    response_delete = client_user_1.delete(f"/api/v1/kittens/{test_kitten_creation[0]["id"]}/")

    assert response_delete.status_code == 204

    # Test DELETE kitten of other user
    response_delete = client_user_1.delete(f"/api/v1/kittens/{test_kitten_creation[1]["id"]}/")

    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_reviews(client_user_1, client_user_2, create_breeds, test_kitten_creation):
    review_payload_1 = {
        "rating": 5,
        "kitten": test_kitten_creation[1]['id']
    }

    # Test review creation
    response = client_user_1.post('/api/v1/reviews/', review_payload_1)

    assert response.status_code == 201
    assert response.data['rating'] == review_payload_1['rating']
    assert response.data['kitten'] == review_payload_1['kitten']

    # Test second review of the same kitten
    response = client_user_1.post('/api/v1/reviews/', review_payload_1)

    assert response.status_code == 400

    # Test review of own kitten
    response = client_user_1.post('/api/v1/reviews/', {"rating": 5, "kitten": test_kitten_creation[0]['id']})

    assert response.status_code == 400

    # Test update of other user review
    response = client_user_2.patch('/api/v1/reviews/1/', {"rating": 3})

    assert response.status_code == 404

    # Test invalid rating
    response = client_user_1.patch(f'/api/v1/reviews/{test_kitten_creation[0]['id']}/', {"rating": 7})
    assert response.status_code == 400

    # Test kitten rating
    response = client_user_1.get(f'/api/v1/kittens/{test_kitten_creation[1]['id']}/')

    assert response.data['reviews_count'] == 1
    assert response.data['rating'] == 5

    # Test DELETE other user review
    response = client_user_2.delete("/api/v1/reviews/1/")
    assert response.status_code == 404

    # Test DELETE of own review
    response = client_user_1.delete("/api/v1/reviews/1/")
    assert response.status_code == 204
