from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from app.infrastructure.db.models import Task, TaskList, User  # noqa: F401

DATABASE_URL = settings.db_url
DEBUG_DB = settings.debug_db

engine = create_engine(DATABASE_URL, echo=DEBUG_DB)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
