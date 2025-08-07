from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.domain.repositories.task import ITaskRepository
from app.graphql.types.task import TaskUpdateInput
from app.infrastructure.db.models.task import Task


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Task]:
        statement = select(Task).options(
            selectinload(Task.assigned_to),
            selectinload(Task.task_list),
        )
        return self.session.exec(statement).all()

    def get_by_task_list_with_filters(
        self,
        list_id: int,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        statement = (
            select(Task)
            .where(Task.task_list_id == list_id)
            .options(
                selectinload(Task.assigned_to),
                selectinload(Task.task_list),
            )
        )

        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)

        return self.session.exec(statement).all()

    def create(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: TaskUpdateInput) -> Task:
        existing_task = self.session.get(Task, task.id)
        if not existing_task:
            raise ValueError("Task not found")

        updates = task.model_dump(exclude_unset=True)

        for attr, value in updates.items():
            if attr != "id" and value is not None:
                setattr(existing_task, attr, value)

        self.session.add(existing_task)
        self.session.commit()
        self.session.refresh(existing_task)
        return existing_task
