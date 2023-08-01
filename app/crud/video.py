from typing import Any

from sqlalchemy import and_, asc, desc, or_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import Session, asc, desc, select

from app import models
from app.models import SubscriptionVideoLink

from .base import BaseCRUD


class VideoCRUD(BaseCRUD[models.Video, models.VideoCreate, models.VideoUpdate]):
    async def get_multi(
        self,
        *args: BinaryExpression[Any],
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        desc_order: bool = True,
        **kwargs: Any,
    ) -> list[models.Video]:
        """
        Retrieve multiple rows from the database that match the given criteria.

        Compared to base method, this adds the 'ordered_by' and 'desc_order' arguments.

        Args:
            db (Session): The database session.
            skip: The number of rows to skip.
            limit: The maximum number of rows to return.
            args: Binary expressions used to filter the rows to be retrieved.
            kwargs: Keyword arguments used to filter the rows to be retrieved.
            order_by: The field to order the results by. Defaults to "created_at".
            desc_order: If True, order in descending order. If False, order in ascending order.

        Returns:
            A list of records that match the given criteria and sorted as per the "order_by" clause.
        """

        order_direction = desc if desc_order else asc

        statement = (
            select(self.model)
            .filter(*args)
            .filter_by(**kwargs)
            .order_by(order_direction(order_by))
            .offset(skip)
            .limit(limit)
        )
        return db.execute(statement).fetchall()


video = VideoCRUD(models.Video)
