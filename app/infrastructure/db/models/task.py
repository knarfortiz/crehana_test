from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_done: bool = False
    status: str = "pending"
    priority: str = "medium"
    task_list_id: Optional[int] = Field(default=None, foreign_key="tasklist.id")
    assigned_to_id: Optional[int] = Field(default=None, foreign_key="user.id")

    task_list: Optional["TaskList"] = Relationship(back_populates="tasks")
    assigned_to: Optional["User"] = Relationship(back_populates="tasks")


class TaskList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tasks: List[Task] = Relationship(back_populates="task_list")
