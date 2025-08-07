import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskListType
from app.graphql.utils import get_task_list_repository
from app.infrastructure.db.models import TaskList


@strawberry.type
class TaskListMutations:
    @strawberry.mutation
    def create_task_list(self, info: Info, name: str) -> TaskListType:
        """
        Creates a new task list

        :param info: The info object passed down from GraphQL
        :param name: The name of the task list
        :return: The created task list
        """
        task_list_repo = get_task_list_repository(info)

        task_list = TaskList(name=name)

        task_list = task_list_repo.create(task_list)

        return TaskListType(id=task_list.id, name=task_list.name, tasks=None)

    @strawberry.mutation
    def update_task_list(self, info: Info, id: int, name: str) -> TaskListType:
        """
        Updates an existing task list

        :param info: The info object passed down from GraphQL
        :param id: The ID of the task list to update
        :param name: The new name for the task list
        :return: The updated task list
        """
        task_list_repo = get_task_list_repository(info)

        task_list = TaskList(id=id, name=name)

        updated_task_list = task_list_repo.update(task_list)

        return TaskListType(
            id=updated_task_list.id, name=updated_task_list.name, tasks=None
        )

    @strawberry.mutation
    def delete_task_list(self, info: Info, list_id: int) -> bool:
        """
        Deletes an existing task list

        :param info: The info object passed down from GraphQL
        :param list_id: The ID of the task list to delete
        :return: True if task list was deleted successfully, False otherwise
        """
        task_list_repo = get_task_list_repository(info)
        try:
            task_list_repo.delete(list_id)
            return True
        except ValueError as e:
            print(e)
            return False
