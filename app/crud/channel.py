from sqlmodel import Session

from app import models

from .base import BaseCRUD


class ChannelCRUD(BaseCRUD[models.Channel, models.ChannelCreate, models.ChannelUpdate]):
    ...


channel = ChannelCRUD(models.Channel)
