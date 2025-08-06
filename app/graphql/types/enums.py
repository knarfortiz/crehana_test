from enum import Enum

import strawberry


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
