from fastapi.testclient import TestClient
from sqlmodel import Session

from python_fastapi_stack import settings
from tests.mock_objects import MOCKED_ITEM_1, MOCKED_ITEMS


def test_create_item(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can create a new item.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 201
    item = response.json()
    assert item["title"] == MOCKED_ITEM_1["title"]
    assert item["description"] == MOCKED_ITEM_1["description"]
    assert item["url"] == MOCKED_ITEM_1["url"]
    assert item["owner_id"] is not None
    assert item["id"] is not None


def test_create_duplicate_item(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test a duplicate item cannot be created.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 201

    # Try to create a duplicate item
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 200
    duplicate = response.json()
    assert duplicate["detail"] == "Item already exists"


def test_read_item(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can read an item.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 201
    created_item = response.json()

    # Read Item
    response = client.get(
        f"{settings.API_V1_PREFIX}/item/{created_item['id']}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    read_item = response.json()

    assert read_item["title"] == MOCKED_ITEM_1["title"]
    assert read_item["description"] == MOCKED_ITEM_1["description"]
    assert read_item["url"] == MOCKED_ITEM_1["url"]
    assert read_item["owner_id"] is not None
    assert read_item["id"] is not None


def test_get_item_not_found(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a item not found error is returned.
    """
    response = client.get(
        f"{settings.API_V1_PREFIX}/item/1",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_get_item_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.get(
        f"{settings.API_V1_PREFIX}/item/5kwf8hFn",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_superuser_get_all_items(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    """
    Test that a superuser can get all items.
    """

    # Create 3 items
    for item in MOCKED_ITEMS:
        response = client.post(
            f"{settings.API_V1_PREFIX}/item/",
            headers=superuser_token_headers,
            json=item,
        )
        assert response.status_code == 201

    # Get all items as superuser
    response = client.get(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3


def test_normal_user_get_all_items(
    db_with_user: Session,  # pylint: disable=unused-argument
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
) -> None:
    """
    Test that a normal user can get all their own items.
    """
    # Create 2 items as normal user
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=normal_user_token_headers,
        json=MOCKED_ITEMS[0],
    )
    assert response.status_code == 201
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=normal_user_token_headers,
        json=MOCKED_ITEMS[1],
    )
    assert response.status_code == 201

    # Create 1 item as super user
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEMS[2],
    )
    assert response.status_code == 201

    # Get all items as normal user
    response = client.get(
        f"{settings.API_V1_PREFIX}/item/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2


def test_update_item(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can update an item.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 201
    created_item = response.json()

    # Update Item
    update_data = MOCKED_ITEM_1.copy()
    update_data["title"] = "Updated Title"
    response = client.patch(
        f"{settings.API_V1_PREFIX}/item/{created_item['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["title"] == update_data["title"]

    # Update wrong item
    response = client.patch(
        f"{settings.API_V1_PREFIX}/item/99999",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 404


def test_update_item_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.patch(
        f"{settings.API_V1_PREFIX}/item/5kwf8hFn",
        headers=normal_user_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """
    Test that a superuser can delete an item.
    """
    response = client.post(
        f"{settings.API_V1_PREFIX}/item/",
        headers=superuser_token_headers,
        json=MOCKED_ITEM_1,
    )
    assert response.status_code == 201
    created_item = response.json()

    # Delete Item
    response = client.delete(
        f"{settings.API_V1_PREFIX}/item/{created_item['id']}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Delete wrong item
    response = client.delete(
        f"{settings.API_V1_PREFIX}/item/99999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_delete_item_forbidden(
    db_with_user: Session, client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """
    Test that a forbidden error is returned.
    """
    response = client.delete(
        f"{settings.API_V1_PREFIX}/item/5kwf8hFn",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"
