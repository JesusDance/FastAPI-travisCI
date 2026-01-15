def test_user_registration(test_client):
    response = test_client.post(
        "/users/",
        json={
            "username": "user1",
            "password": "12345"
        }
    )
    json_response = response.json()

    assert "id" in json_response
    assert "username" in json_response
    assert "password" not in json_response
    assert response.status_code == 200


def test_invalid_user_registration(test_client):
    response = test_client.post(
        "/users/",
        json={
            "username": "Bob",
            "password": "123"
        }
    )
    json_response = response.json()

    assert response.status_code == 422
    assert json_response["detail"][0]["loc"][-1] == "password"
    assert json_response["detail"][0]["msg"] == "String should have at least 4 characters"


def test_dublicate_user_registration(test_client):
    test_client.post(
        "/users/",
        json={
            "username": "user1",
            "password": "1234"
        }
    )
    response = test_client.post(
        "/users/",
        json={
            "username": "user1",
            "password": "1234"
        }
    )
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "Username already exists"


def test_valid_login(test_client, create_test_db):
    response = test_client.post(
        "/users/login/",
        json={
            "username": "Mary",
            "password": "some_password"
        }
    )
    json_response = response.json()

    assert response.status_code == 200
    assert "access_token" in json_response


def test_invalid_login(test_client, create_test_db):
    response = test_client.post(
        "/users/login/",
        json={
            "username": "Mary",
            "password": "12345"
        }
    )
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "Incorrect username or password"
