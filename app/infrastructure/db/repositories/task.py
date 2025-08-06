from typing import List, Optional

from sqlmodel import Session, select

from app.domain.repositories.task import ITaskRepository
from app.infrastructure.db.models.task import Task


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Task]:
        return self.session.exec(select(Task)).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def create(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task_by_list_id(self, list_id: int) -> List[Task]:
        statement = select(Task).where(Task.task_list_id == list_id)
        return self.session.exec(statement).all()
