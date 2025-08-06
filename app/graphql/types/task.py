from __future__ import annotations

from typing import Optional

import strawberry

from app.graphql.types.enums import TaskPriority, TaskStatus
from app.graphql.types.user import UserType


@strawberry.type
class TaskType:
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    status: TaskStatus
    priority: TaskPriority
    assigned_to: Optional["UserType"]
    task_list: Optional["TaskListType"]


from app.graphql.types.task_list import TaskListType
