from typing import List, Optional

import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskPriority, TaskStatus, TaskType
from app.graphql.types.task_list import TaskListType
from app.graphql.types.user import UserType
from app.graphql.utils import get_task_repository


@strawberry.type
class TaskQueries:
    @strawberry.field
    def tasks(self, info: Info) -> List[TaskType]:
        task_repo = get_task_repository(info)

        db_tasks = task_repo.get_all()

        return [
            TaskType(
                id=task.id,
                title=task.title,
                description=task.description,
                is_done=task.is_done,
                status=TaskStatus(task.status),
                priority=TaskPriority(task.priority),
                task_list=(
                    TaskListType(
                        id=task.task_list.id, name=task.task_list.name, tasks=None
                    )
                    if task.task_list
                    else None
                ),
                assigned_to=(
                    UserType(
                        id=task.assigned_to.id,
                        username=task.assigned_to.username,
                        email=task.assigned_to.email,
                    )
                    if task.assigned_to
                    else None
                ),
            )
            for task in db_tasks
        ]

    @strawberry.field
    def task_list_with_filters(
        self,
        info: Info,
        list_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[TaskType]:
        task_repo = get_task_repository(info)
        tasks = task_repo.get_by_task_list_with_filters(
            list_id=list_id,
            status=status.value if status else None,
            priority=priority.value if priority else None,
        )

        return [
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
            for task in tasks
        ]
