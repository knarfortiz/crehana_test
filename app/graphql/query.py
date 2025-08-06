import strawberry

from app.graphql.queries.task import TaskQueries
from app.graphql.queries.user import UserQueries


@strawberry.type
class Query(TaskQueries, UserQueries):
    pass
