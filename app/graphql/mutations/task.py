from typing import Optional

import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskPriority, TaskStatus, TaskType, TaskUpdateInput
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

    @strawberry.mutation
    def update_task(
        self,
        info: Info,
        id: int,
        title: Optional[str] = None,
        is_done: Optional[bool] = None,
        assigned_to_id: Optional[int] = None,
        task_list_id: Optional[int] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> TaskType:
        task_repo = get_task_repository(info)

        task = TaskUpdateInput(
            id=id,
            title=title,
            description=description,
            status=status.value if status is not None else None,
            priority=priority.value if priority is not None else None,
            is_done=is_done,
            assigned_to_id=assigned_to_id,
            task_list_id=task_list_id,
        )

        updated_task = task_repo.update(task)
        return TaskType(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_done=updated_task.is_done,
            status=TaskStatus(updated_task.status),
            priority=TaskPriority(updated_task.priority),
            assigned_to=None,
            task_list=None,
        )

    @strawberry.mutation
    def delete_task(self, info: Info, id: int) -> bool:
        task_repo = get_task_repository(info)

        try:
            task_repo.delete(id)
            return True
        except ValueError as e:
            return e
