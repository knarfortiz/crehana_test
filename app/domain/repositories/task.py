from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]: ...

    @abstractmethod
    def get_by_task_list_with_filters(
        self,
        list_id: int,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Task]: ...

    @abstractmethod
    def create(self, task: Task) -> Task: ...

    @abstractmethod
    def update(self, task: Task) -> Task: ...

    @abstractmethod
    def delete(self, task_id: int) -> None: ...
