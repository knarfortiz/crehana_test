from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]: ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]: ...

    @abstractmethod
    def create(self, task: Task) -> Task: ...

    @abstractmethod
    def get_task_by_list_id(self, list_id: int) -> List[Task]: ...
