from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session

from python_fastapi_stack import crud, models
from tests.mock_objects import MOCKED_ITEM_1, MOCKED_ITEMS


async def get_mocked_item(db: Session) -> models.Item:
    """
    Create a mocked item.
    """
    # Create an item with an owner
    owner = await crud.user.get(db=db, username="test_user")
    item_create = models.ItemCreate(**MOCKED_ITEM_1)

    return await crud.item.create_with_owner_id(db=db, obj_in=item_create, owner_id=owner.id)


async def test_create_item(db_with_user: Session) -> None:
    """
    Test creating a new item with an owner.
    """
    created_item = await get_mocked_item(db=db_with_user)

    # Check the item was created
    assert created_item.title == MOCKED_ITEM_1["title"]
    assert created_item.description == MOCKED_ITEM_1["description"]
    assert created_item.owner_id is not None


async def test_get_item(db_with_user: Session) -> None:
    """
    Test getting an item by id.
    """
    created_item = await get_mocked_item(db=db_with_user)

    # Get the item
    db_item = await crud.item.get(db=db_with_user, id=created_item.id)
    assert db_item
    assert db_item.id == created_item.id
    assert db_item.title == created_item.title
    assert db_item.description == created_item.description
    assert db_item.owner_id == created_item.owner_id


async def test_update_item(db_with_user: Session) -> None:
    """
    Test updating an item.
    """
    created_item = await get_mocked_item(db=db_with_user)

    # Update the item
    db_item = await crud.item.get(db=db_with_user, id=created_item.id)
    db_item_update = models.ItemUpdate(description="New Description")
    updated_item = await crud.item.update(
        db=db_with_user, id=created_item.id, obj_in=db_item_update
    )
    assert db_item.id == updated_item.id
    assert db_item.title == updated_item.title
    assert updated_item.description == "New Description"
    assert db_item.owner_id == updated_item.owner_id


async def test_update_item_without_filter(db_with_user: Session) -> None:
    """
    Test updating an item without a filter.
    """
    created_item = await get_mocked_item(db=db_with_user)

    # Update the item (without a filter)
    await crud.item.get(db=db_with_user, id=created_item.id)
    db_item_update = models.ItemUpdate(description="New Description")
    with pytest.raises(ValueError):
        await crud.item.update(db=db_with_user, obj_in=db_item_update)


async def test_delete_item(db_with_user: Session) -> None:
    """
    Test deleting an item.
    """
    created_item = await get_mocked_item(db=db_with_user)

    # Delete the item
    await crud.item.remove(db=db_with_user, id=created_item.id)
    with pytest.raises(crud.RecordNotFoundError):
        await crud.item.get(db=db_with_user, id=created_item.id)


async def test_delete_item_delete_error(db_with_user: Session, mocker: MagicMock) -> None:
    """
    Test deleting an item with a delete error.
    """
    mocker.patch("python_fastapi_stack.crud.item.get", return_value=None)
    with pytest.raises(crud.DeleteError):
        await crud.item.remove(db=db_with_user, id="00000001")


async def test_get_all_items(db_with_user: Session) -> None:
    """
    Test getting all items.
    """
    # Create some items
    for i, item in enumerate(MOCKED_ITEMS):
        item_create = models.ItemCreate(**item)
        await crud.item.create_with_owner_id(
            db=db_with_user, obj_in=item_create, owner_id=f"0000000{i}"
        )

    # Get all items
    items = await crud.item.get_all(db=db_with_user)
    assert len(items) == len(MOCKED_ITEMS)
