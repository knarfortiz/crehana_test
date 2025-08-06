from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.models.task import TaskList


class ITaskListRepository(ABC):
    @abstractmethod
    def create(self, task_list: TaskList) -> TaskList: ...

    @abstractmethod
    def get_by_id(self, list_id: int) -> Optional[TaskList]: ...

    @abstractmethod
    def get_all(self) -> List[TaskList]: ...

    @abstractmethod
    def update(self, task_list: TaskList) -> TaskList: ...

    @abstractmethod
    def delete(self, list_id: int) -> None: ...
