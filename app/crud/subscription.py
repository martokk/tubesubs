from sqlmodel import Session

from app import models

from .base import BaseCRUD


class SubscriptionCRUD(
    BaseCRUD[models.Subscription, models.SubscriptionCreate, models.SubscriptionUpdate]
):
    async def create_with_user_id(
        self, db: Session, *, obj_in: models.SubscriptionCreate, user_id: str
    ) -> models.Subscription:
        """
        Create a new subscription with an user_id.

        Args:
            db (Session): The database session.
            obj_in (models.VideoCreate): The video to create.
            user_id (str): The user_id to set on the video.

        Returns:
            models.Subscription: The created Subscription.
        """
        obj_in.created_by = user_id
        return await self.create(db, obj_in=obj_in)

    async def get_multi_by_user_id(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> list[models.Subscription]:
        """
        Retrieve multiple subscriptions by user_id.

        Args:
            db (Session): The database session.
            user_id (str): The user_id to filter by.
            skip (int): The number of rows to skip. Defaults to 0.
            limit (int): The maximum number of rows to return. Defaults to 100.

        Returns:
            list[models.Subscription]: A list of subscription that match the given criteria.
        """
        return await self.get_multi(db=db, created_by=user_id, skip=skip, limit=limit)


subscription = SubscriptionCRUD(models.Subscription)
