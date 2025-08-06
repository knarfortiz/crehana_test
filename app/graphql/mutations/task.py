from typing import Optional

import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskPriority, TaskStatus, TaskType
from app.graphql.utils import get_task_repository, get_user_repository
from app.infrastructure.db.models import Task


@strawberry.type
class TaskMutations:
    @strawberry.mutation
    def create_task(
        self,
        info: Info,
        title: str,
        assigned_to_id: int,
        task_list_id: int,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.pending,
        priority: TaskPriority = TaskPriority.medium,
    ) -> TaskType:
        task_repo = get_task_repository(info)
        user_repo = get_user_repository(info)

        task = Task(
            title=title,
            description=description,
            status=status.value,
            priority=priority.value,
            is_done=False,
            assigned_to_id=assigned_to_id,
            task_list_id=task_list_id,
        )

        task = task_repo.create_task(task)

        assigned_user = user_repo.get_by_id(assigned_to_id) if assigned_to_id else None
        task_list = (
            task_repo.get_task_list_by_id(task_list_id) if task_list_id else None
        )

        return TaskType(
            id=task.id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            status=TaskStatus(task.status),
            priority=TaskPriority(task.priority),
            assigned_to=assigned_user,
            task_list=task_list,
        )
