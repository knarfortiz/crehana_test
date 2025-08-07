from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.domain.repositories.task_list import ITaskListRepository
from app.infrastructure.db.models.task import Task, TaskList


class TaskListRepository(ITaskListRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, task_list: TaskList) -> TaskList:
        """
        Creates a new task list and adds it to the database.

        Args:
            task_list: The task list to create.

        Returns:
            The created task list.
        """
        self.session.add(task_list)
        self.session.commit()
        self.session.refresh(task_list)
        return task_list

    def get_by_id(self, list_id: int) -> Optional[TaskList]:
        """
        Retrieves a task list by its ID.

        Args:
            list_id: The ID of the task list to retrieve.

        Returns:
            A TaskList object containing the details of the task list and its tasks,
            or None if the task list is not found.
        """
        statement = (
            select(TaskList)
            .where(TaskList.id == list_id)
            .options(selectinload(TaskList.tasks).selectinload(Task.assigned_to))
        )
        return self.session.exec(statement).one_or_none()

    def get_all(self) -> List[TaskList]:
        """
        Retrieves all task lists from the database.

        Returns:
            A list of TaskList objects containing all task lists and their tasks.
        """
        statement = select(TaskList).options(
            selectinload(TaskList.tasks).selectinload(Task.assigned_to)
        )
        return self.session.exec(statement).all()

    def update(self, task_list: TaskList) -> TaskList:
        """
        Updates a task list.

        Args:
            task_list: The task list to update, including its new name.

        Returns:
            The updated task list.

        Raises:
            ValueError: If the task list does not exist.
        """
        db_task_list = self.session.get(TaskList, task_list.id)
        if not db_task_list:
            raise ValueError(f"TaskList with id {task_list.id} does not exist.")

        if task_list.name is not None:
            db_task_list.name = task_list.name

        self.session.add(db_task_list)
        self.session.commit()
        self.session.refresh(db_task_list)
        return db_task_list

    def delete(self, list_id: int) -> None:
        """
        Deletes a task list.

        Args:
            list_id: The ID of the task list to delete.

        Raises:
            ValueError: If the task list does not exist.
        """
        task_list = self.session.get(TaskList, list_id)
        if task_list:
            self.session.delete(task_list)
            self.session.commit()
        else:
            raise ValueError(f"TaskList with id {list_id} does not exist.")
