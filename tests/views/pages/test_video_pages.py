from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Cookies
from sqlmodel import Session

from python_fastapi_stack import crud, models, settings
from tests.mock_objects import MOCKED_ITEM_1, MOCKED_ITEMS


@pytest.fixture(name="item_1")
async def fixture_item_1(db_with_user: Session) -> models.Item:
    """
    Create an item for testing.
    """
    user = await crud.user.get(db=db_with_user, username="test_user")
    item_create = models.ItemCreate(**MOCKED_ITEM_1)
    return await crud.item.create_with_owner_id(
        db=db_with_user, obj_in=item_create, owner_id=user.id
    )


@pytest.fixture(name="items")
async def fixture_items(db_with_user: Session) -> list[models.Item]:
    """
    Create an item for testing.
    """
    # Create 1 as a superuser
    user = await crud.user.get(db=db_with_user, username=settings.FIRST_SUPERUSER_USERNAME)
    items = []
    item_create = models.ItemCreate(**MOCKED_ITEM_1)
    items.append(
        await crud.item.create_with_owner_id(db=db_with_user, obj_in=item_create, owner_id=user.id)
    )

    # Create 2 as a normal user
    user = await crud.user.get(db=db_with_user, username="test_user")
    for mocked_item in [MOCKED_ITEMS[1], MOCKED_ITEMS[2]]:
        item_create = models.ItemCreate(**mocked_item)
        items.append(
            await crud.item.create_with_owner_id(
                db=db_with_user, obj_in=item_create, owner_id=user.id
            )
        )
    return items


def test_create_item_page(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that the create item page is returned.
    """
    client.cookies = normal_user_cookies
    response = client.get("/items/create")
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/create.html"  # type: ignore


def test_handle_create_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can create a new item.
    """
    client.cookies = normal_user_cookies
    response = client.post(
        "/items/create",
        data=MOCKED_ITEM_1,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/list.html"  # type: ignore


@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
def test_create_duplicate_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    item_1: models.Item,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:  # pytest:
    """
    Test a duplicate item cannot be created.
    """
    # Try to create a duplicate item
    with pytest.raises(Exception):
        response = client.post(
            "/items/create",
            data=MOCKED_ITEM_1,
        )


def test_read_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    item_1: models.Item,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can read an item.
    """
    # Read the item
    response = client.get(
        f"/item/{item_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/view.html"  # type: ignore


def test_get_item_not_found(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a item not found error is returned.
    """
    client.cookies = normal_user_cookies

    # Read the item
    response = client.get("/item/8675309")
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == "/items"


def test_get_item_forbidden(
    db_with_user: Session,  # pylint: disable=unused-argument
    item_1: models.Item,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a forbidden error is returned when a user tries to read an item
    """
    client.cookies = normal_user_cookies

    # Read the item
    response = client.get(
        f"/item/{item_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/view.html"  # type: ignore

    # Logout
    response = client.get(
        "/logout",
    )
    assert response.status_code == status.HTTP_200_OK

    # Attempt Read the item
    response = client.get(
        f"/item/{item_1.id}",  # type: ignore
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_normal_user_get_all_items(
    db_with_user: Session,  # pylint: disable=unused-argument
    items: list[models.Item],  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
    superuser_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a normal user can get all their own items.
    """

    # List all items as normal user
    client.cookies = normal_user_cookies
    response = client.get(
        "/items",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/list.html"  # type: ignore

    # Assert only 2 items are returned (not the superuser's item)
    assert len(response.context["items"]) == 2  # type: ignore


def test_edit_item_page(
    db_with_user: Session,  # pylint: disable=unused-argument
    item_1: models.Item,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that the edit item page is returned.
    """
    client.cookies = normal_user_cookies
    response = client.get(
        f"/item/{item_1.id}/edit",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/edit.html"  # type: ignore

    # Test invalid item id
    response = client.get(
        f"/item/invalid_user_id/edit",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_302_FOUND
    assert response.context["alerts"].danger[0] == "Item not found"  # type: ignore
    assert response.url.path == "/items"


def test_update_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    item_1: models.Item,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can update an item.
    """
    client.cookies = normal_user_cookies

    # Update the item
    response = client.post(
        f"/item/{item_1.id}/edit",  # type: ignore
        data=MOCKED_ITEMS[1],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/edit.html"  # type: ignore

    # View the item
    response = client.get(
        f"/item/{item_1.id}",  # type: ignore
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/view.html"  # type: ignore
    assert response.context["item"].title == MOCKED_ITEMS[1]["title"]  # type: ignore
    assert response.context["item"].description == MOCKED_ITEMS[1]["description"]  # type: ignore
    assert response.context["item"].url == MOCKED_ITEMS[1]["url"]  # type: ignore

    # Test invalid item id
    response = client.post(
        f"/item/invalid_user_id/edit",  # type: ignore
        data=MOCKED_ITEMS[1],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.context["alerts"].danger[0] == "Item not found"  # type: ignore
    assert response.url.path == "/items"


def test_delete_item(
    db_with_user: Session,  # pylint: disable=unused-argument
    item_1: models.Item,
    client: TestClient,
    normal_user_cookies: Cookies,
) -> None:
    """
    Test that a user can delete an item.
    """
    client.cookies = normal_user_cookies

    # Delete the item
    response = client.get(
        f"/item/{item_1.id}/delete",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.url.path == "/items"

    # View the item
    response = client.get(
        f"/item/{item_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.context["alerts"].danger == ["Item not found"]  # type: ignore

    # Test invalid item id
    response = client.get(
        f"/item/invalid_user_id/delete",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
    assert response.context["alerts"].danger[0] == "Item not found"  # type: ignore
    assert response.url.path == "/items"

    # Test DeleteError
    with patch("python_fastapi_stack.crud.item.remove", side_effect=crud.DeleteError):
        response = client.get(
            f"/item/123/delete",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.history[0].status_code == status.HTTP_303_SEE_OTHER
        assert response.context["alerts"].danger[0] == "Error deleting item"  # type: ignore


def test_list_all_items(
    db_with_user: Session,  # pylint: disable=unused-argument
    items: list[models.Item],  # pylint: disable=unused-argument
    client: TestClient,
    superuser_cookies: Cookies,
) -> None:  # sourcery skip: extract-duplicate-method
    """
    Test that a superuser can get all items.
    """

    # List all items as superuser
    client.cookies = superuser_cookies
    response = client.get(
        "/items/all",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "item/list.html"  # type: ignore

    # Assert all 3 items are returned
    assert len(response.context["items"]) == 3  # type: ignore
