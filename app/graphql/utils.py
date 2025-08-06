from strawberry.types import Info

from app.infrastructure.db.repositories.task import TaskRepository


def get_task_repository(info: Info) -> TaskRepository:
    return TaskRepository(info.context["session"])


# def get_user_repo(info: Info) -> UserRepository:
#     return UserRepository(info.context["session"])