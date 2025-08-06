from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.types.enums import TaskPriority, TaskStatus
from app.graphql.types.task import TaskType
from app.graphql.types.task_list import TaskListType
from app.graphql.utils import (
    get_task_list_repository,
    get_task_repository,
    get_user_repository,
)


@strawberry.type
class TaskListQueries:
    @strawberry.field
    def tasks_list(self, info: Info) -> List[TaskListType]:
        task_list_repo = get_task_list_repository(info)
        task_repo = get_task_repository(info)
        user_repo = get_user_repository(info)

        db_task_lists = task_list_repo.get_all()

        result = []

        for task_list in db_task_lists:
            tasks = task_repo.get_task_by_list_id(task_list.id)

            task_types = [
                TaskType(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    is_done=task.is_done,
                    status=TaskStatus(task.status),
                    priority=TaskPriority(task.priority),
                    task_list=None,
                    assigned_to=(
                        user_repo.get_by_id(task.assigned_to_id)
                        if task.assigned_to_id
                        else None
                    ),
                )
                for task in tasks
            ]

            result.append(
                TaskListType(id=task_list.id, name=task_list.name, tasks=task_types)
            )

        return result
