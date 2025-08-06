import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import UserType
from app.infrastructure.db.models import User
from app.infrastructure.db.repositories.user import create_user


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def create_user(
        self,
        info: Info,
        username: str,
        email: str,
    ) -> UserType:
        session: Session = info.context["session"]

        user = User(username=username, email=email)
        user = create_user(session, user)

        return UserType(id=user.id, username=user.username, email=user.email)
