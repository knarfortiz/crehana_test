import strawberry

from app.graphql.mutations.task import TaskMutations
from app.graphql.mutations.user import UserMutations


@strawberry.type
class Mutation(TaskMutations, UserMutations):
    pass
