from typing import List, Optional

from sqlmodel import Session, select

from app.infrastructure.db.models import Task


def get_all_tasks(session: Session) -> List[Task]:
    return session.exec(select(Task)).all()

def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def create_task(session: Session, task: Task) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
