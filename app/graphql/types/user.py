import strawberry


@strawberry.type
class UserType:
    id: int
    username: str
    email: str


@strawberry.type
class UserTokenType:
    token: str
    type: str = "Bearer"
