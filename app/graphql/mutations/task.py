from typing import Optional

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import TaskPriority, TaskStatus, TaskType
from app.graphql.types.task import TaskListType
from app.infrastructure.db.models import Task, TaskList
from app.infrastructure.db.repositories.task import (
    create_task,
    create_task_list,
    get_task_list_by_id,
)
from app.infrastructure.db.repositories.user import get_user_by_id


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
        assigned_to_id: Optional[int] = None,
        task_list_id: Optional[int] = None,
    ) -> TaskType:
        session: Session = info.context["session"]

        task = Task(
            title=title,
            description=description,
            status=status.value,
            priority=priority.value,
            is_done=False,
            assigned_to_id=assigned_to_id,
            task_list_id=task_list_id,
        )

        task = create_task(session, task)

        assigned_user = (
            get_user_by_id(session, assigned_to_id) if assigned_to_id else None
        )
        task_list = get_task_list_by_id(session, task_list_id) if task_list_id else None

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
    def create_list_task(self, info: Info, name: str) -> TaskListType:
        session: Session = info.context["session"]

        task_list = TaskList(name=name)

        task_list = create_task_list(session, task_list)

        return TaskListType(id=task_list.id, name=task_list.name)
