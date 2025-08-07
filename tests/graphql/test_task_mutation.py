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
        status
        isDone
      }
    }
    """

    response = client.post("", json={"query": query})
    data = response.json()["data"]["createTask"]

    assert data["title"] == "Tarea de prueba"
    assert data["description"] == "Hecha desde test"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert data["isDone"] is False


def test_update_task(client):
    create_user_query = """
    mutation {
      createUser(username: "testuser", email: "user@test.com") {
        id
      }
    }
    """
    user_response = client.post("", json={"query": create_user_query})
    user_id = user_response.json()["data"]["createUser"]["id"]

    create_list_query = """
    mutation {
      createTaskList(name: "Tareas de test") {
        id
      }
    }
    """
    list_response = client.post("", json={"query": create_list_query})
    list_id = list_response.json()["data"]["createTaskList"]["id"]

    create_task_query = f"""
    mutation {{
      createTask(
        title: "Tarea de prueba"
        description: "Hecha desde test"
        priority: high
        taskListId: {list_id}
        assignedToId: {user_id}
      ) {{
        id
        title
        description
        priority
        status
        isDone
      }}
    }}
    """
    create_response = client.post("", json={"query": create_task_query})
    assert create_response.status_code == 200
    task_id = create_response.json()["data"]["createTask"]["id"]

    update_query = f"""
    mutation {{
      updateTask(
        id: {task_id}
        title: "Tarea modificada"
        description: "Descripción actualizada"
        isDone: true
        status: completed
        priority: medium
      ) {{
        id
        title
        description
        isDone
        status
        priority
      }}
    }}
    """
    update_response = client.post("", json={"query": update_query})
    assert update_response.status_code == 200
    updated = update_response.json()["data"]["updateTask"]

    assert updated["id"] == task_id
    assert updated["title"] == "Tarea modificada"
    assert updated["description"] == "Descripción actualizada"
    assert updated["isDone"] is True
    assert updated["status"] == "completed"
    assert updated["priority"] == "medium"
