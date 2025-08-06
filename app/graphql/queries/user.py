from typing import List

import strawberry

from app.graphql.types import UserType


@strawberry.type
class UserQueries:
    @strawberry.field
    def users(self) -> List[UserType]:
        return [
            UserType(
                id=1,
                username="francisco",
                email="fran@example.com",
            )
        ]
