from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session

from python_fastapi_stack import crud, models


async def test_create_item(db_with_user: Session) -> None:
    """
    Test creating a new item with an owner.
    """
    owner = await crud.user.get(db=db_with_user, username="test_user")
    video_create = models.VideoCreate(
        id="12345678",
        uploader="test",
        uploader_id="test_uploader_id",
        title="Example Video AAA",
        description="This is example video AAA.",
        duration=417,
        thumbnail="https://sp.rmbl.ws/s8d/R/0_FRh.oq1b.jpg",
        url="https://rumble.com/AAA/test.html",
    )
    video = await crud.video.create_with_owner_id(
        db=db_with_user, in_obj=video_create, owner_id=owner.id
    )
    assert video.title == "Example Video AAA"
    assert video.description == "This is example video AAA."
    assert video.owner_id == owner.id


async def test_get_item(db_with_videos: Session) -> None:
    """
    Test getting an item by id.
    """
    db_video = await crud.video.get(db=db_with_videos, id="00000000")
    assert db_video
    assert db_video.id == "00000000"
    assert db_video.title == "Example Video 0"
    assert db_video.description == "This is example video 0."
    assert db_video.owner_id == "ZbFPeSXW"


async def test_update_item(db_with_videos: Session) -> None:
    """
    Test updating an item.
    """
    db_video = await crud.video.get(db=db_with_videos, id="00000000")
    db_video_update = models.VideoUpdate(description="New Description")
    updated_video = await crud.video.update(
        db=db_with_videos, id="00000000", in_obj=db_video_update
    )
    assert db_video.id == updated_video.id
    assert db_video.title == updated_video.title
    assert updated_video.description == "New Description"
    assert db_video.owner_id == updated_video.owner_id


async def test_update_item_without_filter(db_with_videos: Session) -> None:
    """
    Test updating an item without a filter.
    """
    await crud.video.get(db=db_with_videos, id="00000000")
    db_video_update = models.VideoUpdate(description="New Description")
    with pytest.raises(ValueError):
        await crud.video.update(db=db_with_videos, in_obj=db_video_update)


async def test_delete_item(db_with_videos: Session) -> None:
    """
    Test deleting an item.
    """
    await crud.video.remove(db=db_with_videos, id="00000000")
    with pytest.raises(crud.RecordNotFoundError):
        await crud.video.get(db=db_with_videos, id="00000000")


async def test_delete_item_delete_error(db_with_videos: Session, mocker: MagicMock) -> None:
    """
    Test deleting an item with a delete error.
    """
    mocker.patch("python_fastapi_stack.crud.video.get", return_value=None)
    with pytest.raises(crud.DeleteError):
        await crud.video.remove(db=db_with_videos, id="00000001")
