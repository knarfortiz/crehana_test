from unittest.mock import patch

from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


@patch("app.graphql.mutations.user.send_login_notification")
def test_login_user(mock_send_email, client):
    create_user_query = """
    mutation {
      createUser(username: "testuser", email: "user@test.com", password: "password") {
        id
      }
    }
    """
    client.post("", json={"query": create_user_query})

    login_query = """
    mutation {
      login(email: "user@test.com", password: "password") {
        token
        type
      }
    }
    """
    response = client.post("", json={"query": login_query})
    data = response.json()["data"]["login"]

    assert "token" in data
    assert data["type"] == "Bearer"

    mock_send_email.assert_called_once_with("user@test.com", "testuser")


@patch("app.graphql.mutations.user.send_login_notification")
def test_me_user(mock_send_email, client):
    create_user_query = """
    mutation {
      createUser(username: "testuser", email: "user@test.com", password: "password") {
        id
      }
    }
    """
    client.post("", json={"query": create_user_query})

    login_query = """
    mutation {
      login(email: "user@test.com", password: "password") {
        token
        type
      }
    }
    """
    response = client.post("", json={"query": login_query})
    data = response.json()["data"]["login"]

    mock_send_email.assert_called_once()

    token = data["token"]

    me_query = """
    query {
      me {
        id
        username
        email
      }
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("", json={"query": me_query}, headers=headers)
    data = response.json()["data"]["me"]

    assert data["username"] == "testuser"
    assert data["email"] == "user@test.com"
