from typing import List

import strawberry
from sqlmodel import Session
from strawberry.types import Info

from app.graphql.types import UserType
from app.infrastructure.db.repositories.user import get_all_users


@strawberry.type
class UserQueries:
    @strawberry.field
    def users(self, info: Info) -> List[UserType]:
        session: Session = info.context["session"]

        users = get_all_users(session)

        return [
            UserType(id=user.id, username=user.username, email=user.email)
            for user in users
        ]
