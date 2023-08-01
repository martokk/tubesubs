from sqlmodel import Session

from app import models

from .base import BaseCRUD


class FilterCRUD(BaseCRUD[models.Filter, models.FilterCreate, models.FilterUpdate]):
    async def add_subscriptions(
        self, db: Session, filter_id: str, subscriptions: list[models.Subscription]
    ) -> models.Filter:
        """
        Add a subscription to a filter.

        Args:
            db (Session): The database session.
            filter_id (str): The id of the filter to add the subscription to.
            subscriptions (list[models.Subscription]): The subscriptions to add to the filter.

        Returns:
            filter (models.Filter): The updated filter.
        """
        db_filter = await self.get(id=filter_id, db=db)
        for subscription in subscriptions:
            db_filter = await self.add_subscription(
                db=db, filter_id=filter_id, subscription=subscription
            )

        return db_filter

    async def add_subscription(
        self, db: Session, filter_id: str, subscription: models.Subscription
    ) -> models.Filter:
        """
        Add a subscription to a filter.

        Args:
            db (Session): The database session.
            filter_id (str): The id of the filter to add the subscription to.
            subscription (models.Subscription): The subscription to add to the filter.

        Returns:
            filter (models.Filter): The updated filter.
        """
        db_filter = await self.get(id=filter_id, db=db)
        db_filter.subscriptions.append(subscription)
        db.commit()
        db.refresh(db_filter)
        return db_filter

    async def update_subscriptions(
        self, db: Session, filter_id: str, subscriptions: list[models.Subscription]
    ) -> models.Filter:
        """
        Add a subscription to a filter.

        Args:
            db (Session): The database session.
            filter_id (str): The id of the filter to add the subscription to.
            subscriptions (list[models.Subscription]): The subscriptions to add to the filter.

        Returns:
            filter (models.Filter): The updated filter.
        """
        db_filter = await self.get(id=filter_id, db=db)
        for subscription in subscriptions:
            if subscription not in db_filter.subscriptions:
                db_filter = await self.add_subscription(
                    db=db, filter_id=filter_id, subscription=subscription
                )
        for subscription in db_filter.subscriptions:
            if subscription not in subscriptions:
                db_filter = await self.delete_subscription(
                    db=db, filter_id=filter_id, subscription=subscription
                )

        return db_filter

    async def delete_subscription(
        self, db: Session, filter_id: str, subscription: models.Subscription
    ) -> models.Filter:
        """
        Add a subscription to a filter.

        Args:
            db (Session): The database session.
            filter_id (str): The id of the filter to add the subscription to.
            subscription (models.Subscription): The subscription to add to the filter.

        Returns:
            filter (models.Filter): The updated filter.
        """
        db_filter = await self.get(id=filter_id, db=db)
        db_filter.subscriptions.remove(subscription)
        db.commit()
        db.refresh(db_filter)
        return db_filter


filter = FilterCRUD(model=models.Filter)
