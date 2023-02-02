from sqlmodel import Session

from python_fastapi_stack import models

from .base import BaseCRUD


class ItemCRUD(BaseCRUD[models.Item, models.ItemCreate, models.ItemUpdate]):
    async def create_with_owner_id(
        self, db: Session, *, obj_in: models.ItemCreate, owner_id: str
    ) -> models.Item:
        """
        Create a new item with an owner_id.

        Args:
            db (Session): The database session.
            obj_in (models.ItemCreate): The item to create.
            owner_id (str): The owner_id to set on the item.

        Returns:
            models.Item: The created item.
        """
        obj_in.owner_id = owner_id
        return await self.create(db, obj_in=obj_in)

    async def get_multi_by_owner_id(
        self, db: Session, *, owner_id: str, skip: int = 0, limit: int = 100
    ) -> list[models.Item]:
        """
        Retrieve multiple items by owner_id.

        Args:
            db (Session): The database session.
            owner_id (str): The owner_id to filter by.
            skip (int): The number of rows to skip. Defaults to 0.
            limit (int): The maximum number of rows to return. Defaults to 100.

        Returns:
            list[models.Item]: A list of items that match the given criteria.
        """
        return await self.get_multi(db=db, owner_id=owner_id, skip=skip, limit=limit)


item = ItemCRUD(models.Item)
