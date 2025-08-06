from abc import ABC, abstractmethod
from typing import List, Optional

from app.infrastructure.db.models import User


class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def create(self, user: User) -> User: ...
