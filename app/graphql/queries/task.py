from typing import List

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import TaskPriority, TaskStatus, TaskType
from app.infrastructure.db.repositories import get_all_tasks


@strawberry.type
class TaskQueries:
    @strawberry.field
    def tasks(self, info: Info) -> List[TaskType]:
        session: Session = info.context["session"]

        db_tasks = get_all_tasks(session)

        return [
            TaskType(
                id=task.id,
                title=task.title,
                description=task.description,
                is_done=task.is_done,
                status=TaskStatus(task.status),
                priority=TaskPriority(task.priority),
                list_id=task.list_id,
                assigned_to=None  # aún no usamos usuarios
            )
            for task in db_tasks
        ]
