from typing import List, Optional

from sqlmodel import Session, select

from app.domain.repositories.user import IUserRepository
from app.infrastructure.db.models import User


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[User]:
        """
        Retrieve all users from the database.

        :return: A list of User objects representing all users in the database.
        """
        return self.session.exec(select(User)).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their id from the database.

        :param user_id: The unique identifier for the user to be retrieved.
        :return: A User object representing the user with the given id, or None if no such user exists.
        """
        return self.session.get(User, user_id)

    def create(self, user: User) -> User:
        """
        Add a new user to the database and commit the transaction.

        :param user: The User object to be added to the database.
        :return: The User object after being added to the database, refreshed with updated state.
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address from the database.

        :param email: The email address to search for.
        :return: A User object representing the user with the given email address, or None if no such user exists.
        """
        return self.session.exec(select(User).where(User.email == email)).first()
