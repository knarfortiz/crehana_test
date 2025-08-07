from tests.config import client_fixture, session_fixture

client_fixture
session_fixture

def test_tasks_list(client):
    create = """
    mutation {
      createTask(
        title: "Tarea de prueba"
        description: "Hecha desde test"
        priority: high
        taskListId: 1
        assignedToId: 1
      ) {
        id
      }
    }
    """
    client.post("", json={"query": create})

    query = """
    query {
      tasks {
        id
        title
        priority
      }
    }
    """
    response = client.post("", json={"query": query})
    assert response.status_code == 200

    data = response.json()["data"]["tasks"]
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(task["title"] == "Tarea de prueba" for task in data)
