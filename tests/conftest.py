"""
Shared pytest fixtures. `conftest.py` is a special filename pytest
automatically discovers — anything defined here is available to every
test file in this folder without needing to import it.

The core idea: tests get their own in-memory database, completely
separate from flagforge.db (your real dev database). This is what lets
you delete flagforge.db entirely and still have every test pass.

'''yield paused the set up code to lets the setup code use the session and
	 cleans up after evey test is done'''

"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
git 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# In-memory SQLite: exists only in RAM for the life of this connection,
# never touches disk, and disappears the moment the test finishes.
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
		poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = TestingSessionLocal()


    yield session 


    session.close()
    Base.metadata.drop_all(engine)

''' fastapi receives the db-session whenever a router calls get_db() pauses to had testclient a fake HTTPS request '''
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


