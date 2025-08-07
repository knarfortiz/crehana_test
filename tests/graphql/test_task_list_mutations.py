from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


def test_create_task_list(client):
    query = """
    mutation {
      createTaskList(name: "Mi lista de tareas") {
        id
        name
        tasks { id }
      }
    }
    """

    response = client.post("", json={"query": query})
    assert response.status_code == 200

    data = response.json()["data"]["createTaskList"]

    assert data["id"] is not None
    assert data["name"] == "Mi lista de tareas"
    assert data["tasks"] is None


def test_update_task_list(client):
    create_query = """
    mutation {
      createTaskList(name: "Lista original") {
        id
        name
      }
    }
    """
    create_response = client.post("", json={"query": create_query})
    task_list_id = create_response.json()["data"]["createTaskList"]["id"]

    update_query = f"""
    mutation {{
      updateTaskList(id: {task_list_id}, name: "Lista actualizada") {{
        id
        name
        tasks {{ id }}
      }}
    }}
    """
    update_response = client.post("", json={"query": update_query})
    assert update_response.status_code == 200

    updated = update_response.json()["data"]["updateTaskList"]

    assert updated["id"] == task_list_id
    assert updated["name"] == "Lista actualizada"
    assert updated["tasks"] is None


def test_delete_task_list(client):
    create_query = """
    mutation {
      createTaskList(name: "Lista para eliminar") {
        id
      }
    }
    """
    create_response = client.post("", json={"query": create_query})
    list_id = create_response.json()["data"]["createTaskList"]["id"]

    delete_query = f"""
    mutation {{
      deleteTaskList(listId: {list_id})
    }}
    """
    delete_response = client.post("", json={"query": delete_query})
    assert delete_response.status_code == 200
    assert delete_response.json()["data"]["deleteTaskList"] is True
