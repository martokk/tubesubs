from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from python_fastapi_stack import crud, models, settings


async def test_get_access_token(db_with_user: Session, client: TestClient) -> None:
    login_data = {
        "username": "test_user",
        "password": "test_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["access_token"]
    assert tokens["refresh_token"]


async def test_get_access_token_bad_password(client: TestClient) -> None:
    login_data = {
        "username": "test_user",
        "password": "bad_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json() == {"detail": "Incorrect username or password"}


async def test_get_access_token_bad_username(client: TestClient) -> None:
    login_data = {
        "username": "bad_user",
        "password": "test_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json() == {"detail": "Incorrect username or password"}


async def test_get_access_token_inactive_user(db_with_user: Session, client: TestClient) -> None:
    db_user = await crud.user.update(
        db=db_with_user, username="test_user", in_obj=models.UserUpdate(is_active=False)
    )
    print(db_user)
    login_data = {
        "username": "test_user",
        "password": "test_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    assert r.status_code == status.HTTP_403_FORBIDDEN


# def test_use_access_token(client: TestClient, superuser_token_headers: Dict[str, str]) -> None:
#     r = client.post(
#         f"{settings.API_V1_PREFIX}/login/test-token",
#         headers=superuser_token_headers,
#     )
#     result = r.json()
#     assert r.status_code == 200
#     assert "email" in result
