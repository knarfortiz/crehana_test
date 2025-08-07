from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


def test_get_users(client):
    user_query = """
    mutation {
      createUser(username: "user_test", email: "user@test.com", password: "password") {
        id
      }
    }
    """
    user_resp = client.post("", json={"query": user_query})
    user_id = user_resp.json()["data"]["createUser"]["id"]

    query = """
    query {
        users {
            id
            username
            email
        }
    }
    """
    response = client.post("", json={"query": query})
    assert response.status_code == 200

    data = response.json()["data"]["users"]
    assert isinstance(data, list)
    assert {"id": user_id, "username": "user_test", "email": "user@test.com"}
