from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.types.user import UserType
from app.graphql.utils import get_user_repository


@strawberry.type
class UserQueries:
    @strawberry.field
    def users(self, info: Info) -> List[UserType]:
        user_repo = get_user_repository(info)

        users = user_repo.get_all()

        return [
            UserType(id=user.id, username=user.username, email=user.email)
            for user in users
        ]
