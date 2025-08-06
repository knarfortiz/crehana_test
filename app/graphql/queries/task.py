from typing import List

import strawberry

from app.graphql.types import TaskType


@strawberry.type
class TaskQueries:
    @strawberry.field
    def tasks(self) -> List[TaskType]:
        return [
            TaskType(
                id=1,
                title="Tarea de prueba",
                description="Descripción demo",
                is_done=False,
                status="pending",
                priority="medium",
                list_id=1,
                assigned_to=None,
            )
        ]
