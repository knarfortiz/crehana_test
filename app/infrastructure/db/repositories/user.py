from typing import List, Optional

from sqlmodel import Session, select

from app.infrastructure.db.models import User


def get_all_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
