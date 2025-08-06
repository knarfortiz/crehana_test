from typing import List, Optional

from sqlmodel import Session, select

from app.domain.repositories.user import IUserRepository
from app.infrastructure.db.models import User


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[User]:
        return self.session.exec(select(User)).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
