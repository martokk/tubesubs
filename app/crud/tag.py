from sqlmodel import Session

from app import models

from .base import BaseCRUD

# from .channel import channel


class TagCRUD(BaseCRUD[models.Tag, models.TagCreate, models.TagUpdate]):
    ...
    # async def add_channel(self, db: Session, channel_id: str, tag_id: str) -> models.Tag:
    #     db_channel = await channel.get(db=db, id=channel_id)
    #     db_tag = await self.get(db=db, id=tag_id)

    #     if db_tag and db_channel:
    #         db_tag.channels.append(db_channel)
    #         db.commit()
    #         db.refresh(db_tag)
    #     return db_tag

    # async def update_channels(
    #     self, db: Session, tag_id: str, channels_ids: list[str]
    # ) -> models.Tag:
    #     db_tag = await self.get(db=db, id=tag_id)

    #     for channel_id in channels_ids:
    #         db_channel = await channel.get(db=db, id=channel_id)
    #         if db_channel not in db_tag.channels:
    #             db_tag = await self.add_channel(db=db, tag_id=tag_id, channel_id=channel_id)

    #     for db_channel in db_tag.channels:
    #         if db_channel.id not in channels_ids:
    #             await self.delete_channel(db=db, tag_id=tag_id, channel_id=db_channel.id)

    #     return db_tag

    # async def delete_channel(self, db: Session, tag_id: str, channel_id: str) -> None:
    #     db_tag = await self.get(db=db, id=tag_id)
    #     db_channel = await channel.get(db=db, id=channel_id)

    #     db_tag.channels.remove(db_channel)
    #     db.commit()
    #     db.refresh(db_tag)


tag = TagCRUD(models.Tag)
