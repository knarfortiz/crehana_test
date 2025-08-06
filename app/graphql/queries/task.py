from typing import List

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import TaskPriority, TaskStatus, TaskType
from app.infrastructure.db.repositories.task import get_all_tasks
from app.infrastructure.db.repositories.user import get_user_by_id


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
                task_list=None,
                assigned_to=(
                    get_user_by_id(session, task.assigned_to_id)
                    if task.assigned_to_id
                    else None
                ),
            )
            for task in db_tasks
        ]
