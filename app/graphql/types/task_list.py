from __future__ import annotations

from typing import Optional

import strawberry


@strawberry.type
class TaskListType:
    id: int
    name: str
    tasks: Optional[list["TaskType"]]


from app.graphql.types.task import TaskType
