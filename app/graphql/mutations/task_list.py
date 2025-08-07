import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskListType
from app.graphql.utils import get_task_list_repository
from app.infrastructure.db.models import TaskList


@strawberry.type
class TaskListMutations:
    @strawberry.mutation
    def create_task_list(self, info: Info, name: str) -> TaskListType:
        task_list_repo = get_task_list_repository(info)

        task_list = TaskList(name=name)

        task_list = task_list_repo.create(task_list)

        return TaskListType(id=task_list.id, name=task_list.name, tasks=None)

    @strawberry.mutation
    def update_task_list(self, info: Info, id: int, name: str) -> TaskListType:
        task_list_repo = get_task_list_repository(info)

        task_list = TaskList(id=id, name=name)

        updated_task_list = task_list_repo.update(task_list)

        return TaskListType(
            id=updated_task_list.id, name=updated_task_list.name, tasks=None
        )

    @strawberry.mutation
    def delete_task_list(self, info: Info, list_id: int) -> bool:
        task_list_repo = get_task_list_repository(info)
        try:
            task_list_repo.delete(list_id)
            return True
        except ValueError as e:
            print(e)
            return False
