from typing import Any

from sqlmodel import SQLModel


class FetchResults(SQLModel):
    subscriptions: int = 0
    added_videos: int = 0
    deleted_videos: int = 0

    def __add__(self, other: Any) -> "FetchResults":
        """
        Add two FetchResults together.

        Args:
            other (Any): The other FetchResults object.

        Returns:
            FetchResults: The sum of the two FetchResults objects.

        Raises:
            TypeError: If the other object is not a FetchResults object.
        """
        if not isinstance(other, FetchResults):
            raise TypeError(f"can't add FetchResult and {type(other)}")
        return FetchResults(
            subscriptions=self.subscriptions + other.subscriptions,
            added_videos=self.added_videos + other.added_videos,
            deleted_videos=self.deleted_videos + other.deleted_videos,
        )
