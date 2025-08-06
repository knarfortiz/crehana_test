import strawberry

from app.graphql.types import TaskType


@strawberry.type
class TaskMutations:
    @strawberry.mutation
    def create_task(self, title: str) -> TaskType:
        return TaskType(
            id=999,
            title=title,
            description=None,
            is_done=False,
            status="pending",
            priority="medium",
            list_id=1,
            assigned_to=None,
        )
