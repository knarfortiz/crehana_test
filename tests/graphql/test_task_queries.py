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


def test_task_list_with_filters(client):
    user_query = """
    mutation {
      createUser(username: "filtrador", email: "filtrador@test.com") {
        id
      }
    }
    """
    user_resp = client.post("", json={"query": user_query})
    user_id = user_resp.json()["data"]["createUser"]["id"]

    list_query = """
    mutation {
      createTaskList(name: "Lista para filtros") {
        id
      }
    }
    """
    list_resp = client.post("", json={"query": list_query})
    list_id = list_resp.json()["data"]["createTaskList"]["id"]

    task_queries = [
        f"""
        mutation {{
          createTask(
            title: "Tarea 1",
            description: "completada y alta",
            priority: high,
            status: completed,
            taskListId: {list_id},
            assignedToId: {user_id}
          ) {{ id }}
        }}
        """,
        f"""
        mutation {{
          createTask(
            title: "Tarea 2",
            description: "pendiente y media",
            priority: medium,
            status: pending,
            taskListId: {list_id},
            assignedToId: {user_id}
          ) {{ id }}
        }}
        """,
    ]

    for q in task_queries:
        client.post("", json={"query": q})

    filter_query = f"""
    query {{
      taskListWithFilters(listId: {list_id}, status: completed) {{
        id
        title
        status
        priority
        assignedTo {{
          id
          username
        }}
      }}
    }}
    """
    response = client.post("", json={"query": filter_query})
    assert response.status_code == 200
    data = response.json()["data"]["taskListWithFilters"]
    assert isinstance(data, list)
    assert all(task["status"] == "completed" for task in data)
    assert all(task["priority"] == "high" for task in data)
    assert len(data) == 1
