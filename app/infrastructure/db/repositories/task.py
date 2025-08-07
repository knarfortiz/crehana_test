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
        """
        Retrieves all tasks from the database.

        This method loads all tasks, including their assigned user and task list.
        It returns a list of all tasks in the database.

        :return: A list of all tasks in the database
        """
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
        """
        Retrieves all tasks in the given task list, filtered by the provided status and priority.

        This method loads all tasks in the given task list, including their assigned user and task list.
        It returns a list of all tasks in the given task list that match the provided status and priority.

        :param list_id: The ID of the task list.
        :param status: The status of the tasks to filter by. Can be None to match all tasks.
        :param priority: The priority of the tasks to filter by. Can be None to match all tasks.
        :return: A list of all tasks in the given task list that match the provided status and priority.
        """
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
        """
        Adds a new task to the database and returns the created task.

        This method saves the provided Task object to the database, commits the transaction,
        and refreshes the task instance to reflect any database-generated values (e.g., ID).

        :param task: The Task object to be added to the database.
        :return: The created Task object with updated fields from the database.
        """
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: TaskUpdateInput) -> Task:
        """
        Updates an existing task in the database.

        This method takes a TaskUpdateInput object and applies the provided changes to the task with the matching ID.
        It returns the updated task.

        :param task: The TaskUpdateInput object containing the changes to apply to the task.
        :return: The updated Task object.
        """
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

    def delete(self, task_id: int) -> None:
        """
        Deletes the task with the given ID.

        This method takes the ID of a task, finds the task in the database, and deletes it.
        If the task does not exist, it raises a ValueError.

        :param task_id: The ID of the task to delete.
        :return: None
        """
        task = self.session.get(Task, task_id)
        if not task:
            raise ValueError("Task not found")

        self.session.delete(task)
        self.session.commit()
