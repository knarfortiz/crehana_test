from enum import Enum
from typing import Optional

import strawberry

from app.graphql.types.user import UserType


@strawberry.enum
class TaskStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

@strawberry.enum
class TaskPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"

@strawberry.type
class TaskType:
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    status: TaskStatus
    priority: TaskPriority
    list_id: int
    assigned_to: Optional[UserType]
