import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.infrastructure.db import base
from app.infrastructure.db.base import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    """
    Creates a test sqlite database in memory, and yields a session that can be used to interact with it.

    This fixture is used to provide a test database for integration tests.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    base.engine = engine
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Provides a TestClient configured to interact with the GraphQL API of the application.

    This fixture is used to provide a client for integration tests.
    """

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    client.base_url = f"{client.base_url}/graphql"
    return client
