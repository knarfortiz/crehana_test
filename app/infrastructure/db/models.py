from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_done: bool = False
    status: str = "pending"
    priority: str = "medium"
    list_id: Optional[int] = Field(default=None, foreign_key="tasklist.id")

    list: Optional["TaskList"] = Relationship(back_populates="tasks")

class TaskList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tasks: List[Task] = Relationship(back_populates="list")
