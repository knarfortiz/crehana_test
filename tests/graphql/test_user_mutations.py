from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


def test_login_user(client):
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
