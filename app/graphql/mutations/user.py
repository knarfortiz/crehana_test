import strawberry

from app.graphql.types import UserType


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def create_user(self, username: str, email: str) -> UserType:
        return UserType(
            id=99,
            username=username,
            email=email,
        )
