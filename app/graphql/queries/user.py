from typing import List

import strawberry
from strawberry.types import Info

from app.graphql.permissions import IsAuthenticated
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

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: Info) -> UserType:
        user = info.context.get("current_user")
        return UserType(id=user.id, username=user.username, email=user.email)
