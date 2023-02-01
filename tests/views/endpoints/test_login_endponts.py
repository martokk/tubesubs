from fastapi.testclient import TestClient
from httpx import Cookies
from sqlmodel import Session


def test_login_page(client: TestClient) -> None:
    response = client.get("/login")
    assert response.status_code == 200


def test_handle_login_success(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test handling login
    """
    client.cookies = normal_user_cookie
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == "root/home.html"  # type: ignore


def test_handle_login_failure(db_with_user: Session, client: TestClient) -> None:
    """
    Test handling login failure
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == "login/login.html"  # type: ignore


def test_logout(db_with_user: Session, client: TestClient, normal_user_cookie: Cookies) -> None:
    """
    Test logout
    """
    # Test that the user is logged in
    client.cookies = normal_user_cookie
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == "root/home.html"  # type: ignore

    # Logout
    response = client.get("/logout")
    assert response.status_code == 200

    # Test that the user is logged out
    assert response.template.name != "root/home.html"  # type: ignore


def test_register_page(client: TestClient) -> None:
    response = client.get("/register")
    assert response.status_code == 200
