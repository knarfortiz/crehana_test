from strawberry.types import Info

from app.infrastructure.db.repositories.task import TaskRepository
from app.infrastructure.db.repositories.task_list import TaskListRepository
from app.infrastructure.db.repositories.user import UserRepository


def get_task_list_repository(info: Info) -> TaskListRepository:
    return TaskListRepository(info.context["session"])


def get_task_repository(info: Info) -> TaskRepository:
    return TaskRepository(info.context["session"])


def get_user_repository(info: Info) -> UserRepository:
    return UserRepository(info.context["session"])
