from sqlmodel import Session, SQLModel, create_engine

from app.infrastructure.db.models import Task, TaskList, User  # noqa: F401

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
