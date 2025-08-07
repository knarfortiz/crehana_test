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
        """
        Returns a list of all users.

        :param info: The info object passed down from GraphQL, containing context like background tasks.
        :return: A list of UserType objects, each containing the id, username, and email of a user.
        """
        user_repo = get_user_repository(info)

        users = user_repo.get_all()

        return [
            UserType(id=user.id, username=user.username, email=user.email)
            for user in users
        ]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: Info) -> UserType:
        """
        Returns the current authenticated user.

        :param info: The info object passed down from GraphQL, containing context like
                    background tasks and the current user.
        :return: A UserType object containing the id, username, and email of the
                authenticated user.
        """
        user = info.context.get("current_user")
        return UserType(id=user.id, username=user.username, email=user.email)
