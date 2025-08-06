from typing import Optional

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import TaskPriority, TaskStatus, TaskType
from app.infrastructure.db.models import Task
from app.infrastructure.db.repositories import create_task


@strawberry.type
class TaskMutations:
    @strawberry.mutation
    def create_task(
        self,
        info: Info,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.pending,
        priority: TaskPriority = TaskPriority.medium,
        list_id: Optional[int] = None,
    ) -> TaskType:
        session: Session = info.context["session"]

        task = Task(
            title=title,
            description=description,
            status=status.value,
            priority=priority.value,
            is_done=False,
            list_id=list_id,
        )

        task = create_task(session, task)

        return TaskType(
            id=task.id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            status=TaskStatus(task.status),
            priority=TaskPriority(task.priority),
            list_id=task.list_id,
            assigned_to=None,
        )
