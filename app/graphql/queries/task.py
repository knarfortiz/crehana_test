from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskPriority, TaskStatus, TaskType
from app.graphql.utils import get_task_repository, get_user_repository


@strawberry.type
class TaskQueries:
    @strawberry.field
    def tasks(self, info: Info) -> List[TaskType]:
        task_repo = get_task_repository(info)
        user_repo = get_user_repository(info)

        db_tasks = task_repo.get_all()

        return [
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
            for task in db_tasks
        ]
