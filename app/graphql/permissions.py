from strawberry.permission import BasePermission
from strawberry.types import Info

from app.infrastructure.auth.jwt_service import decode_access_token
from app.infrastructure.db.base import get_session
from app.infrastructure.db.models import User


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        request = info.context["request"]
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        if payload is None:
            return False

        user_id = payload.get("id")
        print(f"Decoded user ID: {user_id}")
        if not user_id:
            return False

        for session in get_session():
            user = session.get(User, int(user_id))
            if user:
                info.context["current_user"] = user
                return True

        return False
