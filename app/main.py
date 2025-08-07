from contextlib import asynccontextmanager
from typing import Any

from fastapi import BackgroundTasks, FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from app.config import settings
from app.graphql.schema import schema
from app.infrastructure.db.base import get_session, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


async def get_context_dependency(request: Request, background_tasks: BackgroundTasks) -> dict[str, Any]:
    session = next(get_session())
    return {"request": request, "session": session, "background_tasks": background_tasks}


graphql_app = GraphQLRouter(schema, context_getter=get_context_dependency)
app.include_router(graphql_app, prefix="/graphql")
