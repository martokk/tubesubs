from sqlmodel import Session

from app import models
from app.crud.tag import tag

from .base import BaseCRUD


class ChannelCRUD(BaseCRUD[models.Channel, models.ChannelCreate, models.ChannelUpdate]):
    async def add_tag(self, db: Session, channel_id: str, tag_id: str) -> models.Channel:
        db_channel = await self.get(db=db, id=channel_id)
        db_tag = await tag.get(db=db, id=tag_id)

        if db_channel and db_tag:
            db_channel.tags.append(db_tag)
            db.commit()
            db.refresh(db_channel)
        return db_channel

    async def update_tags(self, db: Session, channel_id: str, tag_ids: list[str]) -> models.Channel:
        db_channel = await self.get(db=db, id=channel_id)

        for tag_id in tag_ids:
            db_tag = await tag.get(db=db, id=tag_id)
            if db_tag not in db_channel.tags:
                db_channel = await self.add_tag(db=db, channel_id=channel_id, tag_id=tag_id)

        for db_tag in db_channel.tags:
            if db_tag.id not in tag_ids:
                await self.delete_tag(db=db, channel_id=channel_id, tag_id=db_tag.id)

        return db_channel

    async def update_tag_of_channels(
        self, db: Session, tag_id: str, channel_ids: list[str]
    ) -> models.Tag:
        db_tag = await tag.get(db=db, id=tag_id)
        db_all_channels = await self.get_all(db=db)

        db_channels = [channel for channel in db_all_channels if channel.id in channel_ids]

        for db_channel in db_channels:
            if db_channel not in db_tag.channels:
                db_tag.channels.append(db_channel)

        for db_channel in db_all_channels:
            if db_channel not in db_channels and db_channel in db_tag.channels:
                db_tag.channels.remove(db_channel)

        db.commit()
        db.refresh(db_tag)
        return db_tag

    async def delete_tag(self, db: Session, channel_id: str, tag_id: str) -> None:
        db_channel = await self.get(db=db, id=channel_id)
        db_tag = await tag.get(db=db, id=tag_id)

        db_channel.tags.remove(db_tag)
        db.commit()
        db.refresh(db_channel)


channel = ChannelCRUD(models.Channel)
