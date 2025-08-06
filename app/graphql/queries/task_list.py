from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.types.enums import TaskPriority, TaskStatus
from app.graphql.types.task import TaskType
from app.graphql.types.task_list import TaskListType
from app.graphql.types.user import UserType
from app.graphql.utils import (
    get_task_list_repository,
)


@strawberry.type
class TaskListQueries:
    @strawberry.field
    def tasks_list(self, info: Info) -> List[TaskListType]:
        task_list_repo = get_task_list_repository(info)
        db_task_lists = task_list_repo.get_all()

        result = []

        for task_list in db_task_lists:
            task_types = [
                TaskType(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    is_done=task.is_done,
                    status=TaskStatus(task.status),
                    priority=TaskPriority(task.priority),
                    assigned_to=(
                        UserType(
                            id=task.assigned_to.id,
                            username=task.assigned_to.username,
                            email=task.assigned_to.email,
                        )
                        if task.assigned_to
                        else None
                    ),
                    task_list=None,
                )
                for task in task_list.tasks
            ]

            result.append(
                TaskListType(id=task_list.id, name=task_list.name, tasks=task_types)
            )

        return result
