import pytest
from fastapi.testclient import TestClient
from httpx import Cookies
from sqlmodel import Session

from tests.mock_objects import MOCKED_ITEM_1, MOCKED_ITEMS


def test_create_item_page(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that the create item page is returned.
    """
    client.cookies = normal_user_cookie
    response = client.get("/items/create")
    assert response.status_code == 200
    assert response.template.name == "item/create.html"  # type: ignore


def test_handle_create_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that a user can create a new item.
    """
    client.cookies = normal_user_cookie
    response = client.post(
        "/items/create",
        data=MOCKED_ITEM_1,
    )
    assert response.status_code == 200
    assert response.template.name == "item/list.html"  # type: ignore


@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
def test_create_duplicate_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:  # pytest:
    """
    Test a duplicate item cannot be created.
    """
    client.cookies = normal_user_cookie
    response = client.post(
        "/items/create",
        data=MOCKED_ITEM_1,
    )
    assert response.status_code == 200

    # Try to create a duplicate item
    with pytest.raises(Exception):
        response = client.post(
            "/items/create",
            data=MOCKED_ITEM_1,
        )


def test_read_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that a user can read an item.
    """
    client.cookies = normal_user_cookie

    # Create an item
    response = client.post(
        "/items/create",
        data=MOCKED_ITEM_1,
    )
    assert response.status_code == 200

    # Read the item
    response = client.get(
        f"/item/{response.context['items'][0].id}",  # type: ignore
    )
    assert response.status_code == 200
    assert response.template.name == "item/view.html"  # type: ignore


def test_get_item_not_found(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that a item not found error is returned.
    """
    client.cookies = normal_user_cookie

    # Read the item
    response = client.get("/item/8675309")
    assert response.status_code == 200
    assert response.url.path == "/items"


def test_get_item_forbidden(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a forbidden error is returned when a user tries to read an item
    """
    client.cookies = normal_user_cookie

    # Create an item
    response = client.post(
        "/items/create",
        data=MOCKED_ITEM_1,
    )
    assert response.status_code == 200
    item_id = response.context["items"][0].id  # type: ignore

    # Read the item
    response = client.get(
        f"/item/{item_id}",
    )
    assert response.status_code == 200
    assert response.template.name == "item/view.html"  # type: ignore

    # Logout
    response = client.get(
        "/logout",
    )
    assert response.status_code == 200

    # Attempt Read the item
    response = client.get(
        f"/item/{item_id}",  # type: ignore
    )
    assert response.status_code == 401


def test_normal_user_get_all_items(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
    superuser_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a normal user can get all their own items.
    """
    client.cookies = normal_user_cookie

    # Create 2 items as normal user
    response = client.post(
        "/items/create",
        data=MOCKED_ITEMS[0],
    )
    assert response.status_code == 200
    response = client.post(
        "/items/create",
        data=MOCKED_ITEMS[1],
    )
    assert response.status_code == 200

    # Create 1 item as superuser
    client.cookies = superuser_cookies
    response = client.post(
        "/items/create",
        data=MOCKED_ITEMS[2],
    )
    assert response.status_code == 200

    # List all items as normal user
    client.cookies = normal_user_cookie
    response = client.get(
        "/items",
    )
    assert response.status_code == 200
    assert response.template.name == "item/list.html"  # type: ignore

    # Assert only 2 items are returned (not the superuser's item)
    assert len(response.context["items"]) == 2  # type: ignore


def test_update_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that a user can update an item.
    """
    client.cookies = normal_user_cookie

    # Create an item
    response = client.post(
        "/items/create",
        data=MOCKED_ITEMS[0],
    )
    assert response.status_code == 200

    # Update the item
    response = client.post(
        f"/item/{response.context['items'][0].id}/edit",  # type: ignore
        data=MOCKED_ITEMS[1],
    )
    assert response.status_code == 200
    assert response.template.name == "item/edit.html"  # type: ignore

    # View the item
    response = client.get(
        f"/item/{response.context['item'].id}",  # type: ignore
    )
    assert response.status_code == 200
    assert response.template.name == "item/view.html"  # type: ignore
    assert response.context["item"].title == MOCKED_ITEMS[1]["title"]  # type: ignore
    assert response.context["item"].description == MOCKED_ITEMS[1]["description"]  # type: ignore
    assert response.context["item"].url == MOCKED_ITEMS[1]["url"]  # type: ignore


def test_delete_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookie: Cookies,
) -> None:
    """
    Test that a user can delete an item.
    """
    client.cookies = normal_user_cookie

    # Create an item
    response = client.post(
        "/items/create",
        data=MOCKED_ITEMS[0],
    )
    assert response.status_code == 200
    item_id = response.context["items"][0].id  # type: ignore

    # Delete the item
    response = client.get(
        f"/item/{item_id}/delete",
    )
    assert response.status_code == 200
    assert response.history[0].status_code == 303
    assert response.url.path == "/items"

    # View the item
    response = client.get(
        f"/item/{item_id}",
    )
    assert response.status_code == 200
    assert response.context["alerts"].danger == ["Item not found"]  # type: ignore
