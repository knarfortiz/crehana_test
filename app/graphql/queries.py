import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "¡Hola desde GraphQL!"
