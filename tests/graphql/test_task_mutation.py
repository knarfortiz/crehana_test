from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


def test_create_task(client):
    query = """
    mutation {
      createTask(
        title: "Tarea de prueba"
        description: "Hecha desde test"
        priority: high
        taskListId: 1
        assignedToId: 1
      ) {
        id
        title
        description
        priority
      }
    }
    """

    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["createTask"]

    assert data["title"] == "Tarea de prueba"
    assert data["priority"] == "high"
