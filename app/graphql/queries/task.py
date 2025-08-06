from typing import List

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import TaskPriority, TaskStatus, TaskType
from app.graphql.utils import get_task_repository
from app.infrastructure.db.repositories.user import get_user_by_id


@strawberry.type
class TaskQueries:
    @strawberry.field
    def tasks(self, info: Info) -> List[TaskType]:
        session: Session = info.context["session"]
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
                task_list=None,
                assigned_to=(
                    get_user_by_id(session, task.assigned_to_id)
                    if task.assigned_to_id
                    else None
                ),
            )
            for task in db_tasks
        ]
