from typing import Optional

import strawberry
from strawberry.types import Info

from app.graphql.types.task import TaskPriority, TaskStatus, TaskType, TaskUpdateInput
from app.graphql.utils import (
    get_task_list_repository,
    get_task_repository,
    get_user_repository,
)
from app.infrastructure.db.models import Task


@strawberry.type
class TaskMutations:
    @strawberry.mutation
    def create_task(
        self,
        info: Info,
        title: str,
        assigned_to_id: int,
        task_list_id: int,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.pending,
        priority: TaskPriority = TaskPriority.medium,
    ) -> TaskType:
        """
        Creates a new task and adds it to the specified task list.

        Parameters:
            info (Info): The execution context information.
            title (str): The title of the task.
            assigned_to_id (int): The ID of the user to whom the task is assigned.
            task_list_id (int): The ID of the task list to which the task belongs.
            description (Optional[str], optional): A brief description of the task. Defaults to None.
            status (TaskStatus, optional): The status of the task. Defaults to TaskStatus.pending.
            priority (TaskPriority, optional): The priority level of the task. Defaults to TaskPriority.medium.

        Returns:
            TaskType: The created task as a TaskType object, including details about the task, its assignee, and its task list.
        """
        task_repo = get_task_repository(info)
        user_repo = get_user_repository(info)
        task_list_repo = get_task_list_repository(info)

        task = Task(
            title=title,
            description=description,
            status=status.value,
            priority=priority.value,
            is_done=False,
            assigned_to_id=assigned_to_id,
            task_list_id=task_list_id,
        )

        task = task_repo.create(task)

        assigned_user = user_repo.get_by_id(assigned_to_id) if assigned_to_id else None
        task_list = task_list_repo.get_by_id(task_list_id) if task_list_id else None

        return TaskType(
            id=task.id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            status=TaskStatus(task.status),
            priority=TaskPriority(task.priority),
            assigned_to=assigned_user,
            task_list=task_list,
        )

    @strawberry.mutation
    def update_task(
        self,
        info: Info,
        id: int,
        title: Optional[str] = None,
        is_done: Optional[bool] = None,
        assigned_to_id: Optional[int] = None,
        task_list_id: Optional[int] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> TaskType:
        """
        Updates a task with the given ID.

        Args:
            id: The ID of the task to update.
            title: The new title of the task. If None, the title remains unchanged.
            is_done: The new status of the task. If None, the status remains unchanged.
            assigned_to_id: The ID of the user to assign to the task. If None, the assigned user remains unchanged.
            task_list_id: The ID of the task list to assign to the task. If None, the task list remains unchanged.
            description: The new description of the task. If None, the description remains unchanged.
            status: The new status of the task. If None, the status remains unchanged.
            priority: The new priority of the task. If None, the priority remains unchanged.

        Returns:
            The updated task.
        """
        task_repo = get_task_repository(info)

        task = TaskUpdateInput(
            id=id,
            title=title,
            description=description,
            status=status.value if status is not None else None,
            priority=priority.value if priority is not None else None,
            is_done=is_done,
            assigned_to_id=assigned_to_id,
            task_list_id=task_list_id,
        )

        updated_task = task_repo.update(task)
        return TaskType(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            is_done=updated_task.is_done,
            status=TaskStatus(updated_task.status),
            priority=TaskPriority(updated_task.priority),
            assigned_to=None,
            task_list=None,
        )

    @strawberry.mutation
    def delete_task(self, info: Info, id: int) -> bool:
        """
        Deletes the task with the given ID.

        Args:
            info (Info): The execution context information.
            id (int): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted, False if the task was not found.
        """
        task_repo = get_task_repository(info)

        try:
            task_repo.delete(id)
            return True
        except ValueError as e:
            print(e)
            return False
