import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    def say_hello(self, name: str) -> str:
        return f"¡Hola, {name}!"
