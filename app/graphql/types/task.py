from __future__ import annotations

from typing import Optional

import strawberry
from pydantic import BaseModel

from app.graphql.types.enums import TaskPriority, TaskStatus
from app.graphql.types.user import UserType


class TaskUpdateInput(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[int] = None
    task_list_id: Optional[int] = None


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
