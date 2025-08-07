from datetime import timedelta

import strawberry
from fastapi import BackgroundTasks
from strawberry.types import Info

from app.graphql.types.user import UserTokenType, UserType
from app.graphql.utils import get_user_repository
from app.infrastructure.auth.jwt_service import create_access_token
from app.infrastructure.auth.password_hasher import hash_password, verify_password
from app.infrastructure.db.models import User
from app.infrastructure.email.fake_sender import send_login_notification


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def create_user(
        self,
        info: Info,
        username: str,
        email: str,
        password: str,
    ) -> UserType:
        """
        Creates a new user.

        :param info: The info object passed down from GraphQL
        :param username: The username for the new user
        :param email: The email for the new user
        :param password: The password for the new user
        :return: The created user
        """
        user_repo = get_user_repository(info)

        user = User(
            username=username, email=email, hashed_password=hash_password(password)
        )
        user = user_repo.create(user)

        return UserType(id=user.id, username=user.username, email=user.email)

    @strawberry.mutation
    def login(self, info: Info, email: str, password: str) -> UserTokenType:
        """
        Authenticates a user and returns a token upon successful login.

        :param info: The info object passed down from GraphQL, containing context like background tasks.
        :param email: The email address of the user attempting to log in.
        :param password: The password for the user attempting to log in.
        :return: A UserTokenType containing the authentication token.
        :raises Exception: If the username or password is invalid.
        """
        user_repo = get_user_repository(info)

        user = user_repo.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise Exception("Invalid username or password")

        token = create_access_token(user.username, user.id, timedelta(minutes=15))

        try:
            background_tasks: BackgroundTasks = info.context["background_tasks"]
            background_tasks.add_task(
                send_login_notification, user.email, user.username
            )
        except Exception as e:
            print(f"Error sending login notification: {e}")

        return UserTokenType(token=token)
