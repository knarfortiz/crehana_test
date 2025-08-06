import strawberry
from strawberry.types import Info

from app.graphql.types.user import UserType
from app.graphql.utils import get_user_repository
from app.infrastructure.db.models import User


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def create_user(
        self,
        info: Info,
        username: str,
        email: str,
    ) -> UserType:
        user_repo = get_user_repository(info)

        user = User(username=username, email=email)
        user = user_repo.create(user)

        return UserType(id=user.id, username=user.username, email=user.email)
