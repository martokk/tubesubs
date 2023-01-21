import datetime
import os
from collections.abc import AsyncGenerator
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from python_fastapi_stack import crud, models, settings
from python_fastapi_stack.api import deps
from python_fastapi_stack.core import security
from python_fastapi_stack.core.app import app
from python_fastapi_stack.db.init_db import create_all, init_initial_data

# from python_fastapi_stack.db.session import SessionLocal


@pytest.fixture(name="db")
async def fixture_db(tmpdir: str, monkeypatch: MagicMock) -> AsyncGenerator[Session, None]:
    """
    Fixture that creates a temporary database file and returns a database session.
    """
    # Set up test database file in a temporary directory
    db_file = Path(tmpdir.join("test_db.sqlite"))

    # Patch the database file path
    monkeypatch.setattr("python_fastapi_stack.paths.DATABASE_FILE", db_file)

    # Ensure the test database does not exist before running the function
    if os.path.exists(db_file):
        os.remove(db_file)

    db_url = f"sqlite:///{db_file}"
    test_engine = create_engine(
        db_url,
        echo=False,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )

    await create_all(engine=test_engine, sqlmodel_create_all=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=Session)

    db = SessionLocal()
    await init_initial_data(db=db)
    # user_create = models.UserCreateWithPassword(
    #     username="test_user", email="test@example.com", password="test_password"
    # )
    # db_user = await crud.user.create_with_password(db=db, in_obj=user_create)
    # print(db_user)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="client")
async def fixture_client(db: Session) -> AsyncGenerator[TestClient, None]:
    # Configure the TestClient to use the temporary database
    app.dependency_overrides[deps.get_db] = lambda: db
    with TestClient(app) as c:
        yield c


@pytest.fixture(name="db_with_user")
async def fixture_db_with_user(db: Session) -> Session:
    """
    Fixture that creates an example user in the test database.

    Args:
        db (Session): database session.

    Returns:
        Session: database session with example user.
    """
    user_hashed_password = security.get_password_hash("test_password")
    user_create = models.UserCreate(
        username="test_user", email="test@example.com", hashed_password=user_hashed_password
    )
    await crud.user.create(in_obj=user_create, db=db)
    return db


@pytest.fixture(name="db_with_videos")
async def fixture_db_with_videos(db_with_user: Session) -> Session:
    """
    Fixture that creates example videos for the example source in the test database.

    Args:
        db_with_user (Session): database session.

    Returns:
        Session: database session with example videos.

    Returns the following video_ids:
        - 5kwf8hFn
        - R6iBBN3J
        - fEpPZMry
    """
    owner = await crud.user.get(db=db_with_user, username="test_user")
    videos = []
    for i in range(3):
        video_create = models.VideoCreate(
            id=f"{i}{i}{i}{i}{i}{i}{i}{i}",
            uploader="test",
            uploader_id="test_uploader_id",
            title=f"Example Video {i}",
            description=f"This is example video {i}.",
            duration=417,
            thumbnail="https://sp.rmbl.ws/s8d/R/0_FRh.oq1b.jpg",
            url=f"https://rumble.com/{i}{i}{i}{i}/test.html",
            added_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        video = await crud.video.create_with_owner_id(
            in_obj=video_create, db=db_with_user, owner_id=owner.id
        )
        videos.append(video)
    return db_with_user


@pytest.fixture(name="superuser_token_headers")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    """
    Fixture that returns the headers for a superuser.
    """
    login_data = {
        "username": settings.FIRST_SUPERUSER_USERNAME,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture(name="normal_user_token_headers")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    """
    Fixture that returns the headers for a normal user.
    """
    login_data = {
        "username": "test_user",
        "password": "test_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture(name="test_request")
def fixture_request() -> Request:
    """
    Fixture that returns a request object.
    """
    return Request(scope={"type": "http", "method": "GET", "path": "/"})
