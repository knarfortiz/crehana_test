import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskListType
from app.graphql.utils import get_task_list_repository
from app.infrastructure.db.models import TaskList


@strawberry.type
class TaskListMutations:
    @strawberry.mutation
    def create_task_list(self, info: Info, name: str) -> TaskListType:
        task_repo = get_task_list_repository(info)

        task_list = TaskList(name=name)

        task_list = task_repo.create(task_list)

        return TaskListType(id=task_list.id, name=task_list.name)

    @strawberry.mutation
    def update_task_list(self, info: Info, id: int, name: str) -> TaskListType:
        task_repo = get_task_list_repository(info)

        task_list = TaskList(id=id, name=name)

        updated_task_list = task_repo.update(task_list)

        return TaskListType(
            id=updated_task_list.id, name=updated_task_list.name, tasks=None
        )
