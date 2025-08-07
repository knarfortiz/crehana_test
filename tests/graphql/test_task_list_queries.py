from tests.config import client_fixture, session_fixture

client_fixture
session_fixture


def test_tasks_list(client):
    create_user_query = """
    mutation {
      createUser(
        username: "usuario_tasklist",
        email: "tasklist@test.com",
        password: "password"
      ) {
        id
      }
    }
    """
    user_resp = client.post("", json={"query": create_user_query})
    user_id = user_resp.json()["data"]["createUser"]["id"]

    create_list_query = """
    mutation {
      createTaskList(name: "Lista con tareas") {
        id
      }
    }
    """
    list_resp = client.post("", json={"query": create_list_query})
    list_id = list_resp.json()["data"]["createTaskList"]["id"]

    create_task_query = f"""
    mutation {{
      createTask(
        title: "Tarea asociada",
        description: "Tarea dentro de lista",
        status: pending,
        priority: low,
        taskListId: {list_id},
        assignedToId: {user_id}
      ) {{
        id
      }}
    }}
    """
    client.post("", json={"query": create_task_query})

    query = """
    query {
      tasksList {
        id
        name
        tasks {
          id
          title
          status
          priority
          assignedTo {
            id
            username
          }
        }
      }
    }
    """
    response = client.post("", json={"query": query})
    assert response.status_code == 200
    data = response.json()["data"]["tasksList"]

    assert isinstance(data, list)
    assert len(data) >= 1
    lista = data[0]
    assert lista["name"] == "Lista con tareas"
    assert isinstance(lista["tasks"], list)
    assert any(task["title"] == "Tarea asociada" for task in lista["tasks"])


def test_task_list_by_id(client):
    user_query = """
    mutation {
      createUser(
        username: "user_test",
        email: "user@test.com",
        password: "password"
      ) {
        id
      }
    }
    """
    user_resp = client.post("", json={"query": user_query})
    user_id = user_resp.json()["data"]["createUser"]["id"]

    list_query = """
    mutation {
      createTaskList(name: "Lista específica") {
        id
      }
    }
    """
    list_resp = client.post("", json={"query": list_query})
    list_id = list_resp.json()["data"]["createTaskList"]["id"]

    task_query = f"""
    mutation {{
      createTask(
        title: "Tarea para lista específica",
        description: "Con usuario asignado",
        status: in_progress,
        priority: medium,
        taskListId: {list_id},
        assignedToId: {user_id}
      ) {{
        id
      }}
    }}
    """
    client.post("", json={"query": task_query})

    query = f"""
    query {{
      taskListById(listId: {list_id}) {{
        id
        name
        tasks {{
          id
          title
          status
          priority
          assignedTo {{
            id
            username
            email
          }}
        }}
      }}
    }}
    """
    response = client.post("", json={"query": query})
    assert response.status_code == 200

    data = response.json()["data"]["taskListById"]
    assert data["id"] == list_id
    assert data["name"] == "Lista específica"
    assert isinstance(data["tasks"], list)
    assert len(data["tasks"]) == 1

    task = data["tasks"][0]
    assert task["title"] == "Tarea para lista específica"
    assert task["status"] == "in_progress"
    assert task["priority"] == "medium"
    assert task["assignedTo"]["id"] == user_id
    assert task["assignedTo"]["username"] == "user_test"


def test_task_list_by_id_not_found(client):
    query = """
    query {
      taskListById(listId: 9999) {
        id
        name
      }
    }
    """
    response = client.post("", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["taskListById"] is None
