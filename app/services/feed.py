import datetime
from pathlib import Path

from feedgen.feed import FeedGenerator

from app import settings
from app.models import Playlist
from app.paths import FEEDS_PATH


def get_published_at(
    created_at: datetime.datetime, released_at: datetime.datetime | None
) -> datetime.datetime:
    """
    Returns an estimated published date.

    Args:
        created_at: The date the video was added to the database.
        released_at: The date the video was released on YouTube.

    Returns:
        The latest date between `released_at` and `created_at`.
    """
    if not released_at:
        return created_at
    if released_at.date() == created_at.date():
        if released_at.time() == datetime.time(0, 0, 0):
            return created_at
    return released_at


class PlaylistFeedGenerator(FeedGenerator):
    def __init__(self, playlist: Playlist):
        """
        Initialize the SourceFeedGenerator object.

        Args:
            playlist: The Playlist to retrieve data from.
        """
        super().__init__()
        # self.load_extension("podcast")
        self.rss_file_path = get_rss_file_path(id=playlist.id)
        self._generate_feed(playlist=playlist)

    def _generate_feed(self, playlist: Playlist) -> None:
        """
        Generate the feed data.

        Args:
            playlist: The playlist to retrieve data from.
        """
        id = playlist.id
        title = playlist.name
        link = f"{settings.BASE_URL}{playlist.feed_url}"
        author = settings.PROJECT_NAME

        # Filter/Source Unique Data
        self.title(title)
        self.link(href=link, rel="self")
        self.id(id)

        # Shared Data
        self.author({"name": author})
        self.link(href=settings.BASE_URL, rel="alternate")
        # self.logo(f"{source_logo}?=.jpg")
        self.subtitle(f"Generated by {settings.PROJECT_NAME}")
        self.description(f"Generated by {settings.PROJECT_NAME}")
        self.pubDate(datetime.datetime.now(tz=datetime.timezone.utc))
        # self.podcast.itunes_author(  # type: ignore # pylint: disable=no-member
        #     itunes_author=author
        # )
        # self.podcast.itunes_image(  # type: ignore # pylint: disable=no-member
        #     itunes_image=f"{source_logo}?=.jpg"
        # )

        # Generate Feed Posts
        for item in playlist.playlist_items:
            # Get Published Date
            published_at = item.created_at  # pragma: no cover

            # Set Post
            post = self.add_entry()
            post.author({"name": author})
            post.id(item.id)
            post.title(item.title)
            post.link(href=item.url)
            post.description(" ")
            # post.enclosure(
            #     url=f"{settings.BASE_URL}{item.feed_media_url}",
            #     length=str(video.media_filesize),
            #     type="video/mp4",
            # )  # TODO: Handle non-mp4 files as well
            post.published(published_at.replace(tzinfo=datetime.timezone.utc))
            # post.podcast.itunes_duration(  # type: ignore # pylint: disable=no-member
            #     itunes_duration=video.duration
            # )
            # post.podcast.itunes_image(  # type: ignore # pylint: disable=no-member
            #     itunes_image=f"{video.thumbnail}?=.jpg"
            # )  # type: ignore # pylint: disable=no-member

    async def save(self) -> Path:
        """
        Saves a generated feed to file.

        Returns:
            The path to the saved file.
        """
        self.rss_file(filename=self.rss_file_path, encoding="UTF-8", pretty=True)
        return self.rss_file_path


# RSS File
def get_rss_file_path(id: str) -> Path:
    """
    Returns the file path for a rss file.

    Args:
        id: The source/filter id to retrieve the file path for.

    Returns:
        The path to the rss file.
    """
    return FEEDS_PATH / f"{id}.rss"


async def get_rss_file(id: str) -> Path:
    """
    Returns a validated rss file.

    Args:
        id: The source/filter id to retrieve the file path for.

    Returns:
        The path to the rss file.

    Raises:
        FileNotFoundError: If the rss file does not exist.
    """
    rss_file = get_rss_file_path(id=id)

    # Validate RSS File exists
    if not rss_file.exists():
        raise FileNotFoundError()
    return rss_file


async def delete_rss_file(id: str) -> None:
    """
    Deletes a rss file.

    Args:
        id: The source/filter id to delete the file for.
    """
    rss_file = get_rss_file_path(id=id)
    rss_file.unlink()


async def build_rss_file(playlist: Playlist) -> Path:
    """
    Builds a .rss file, saves it to disk.

    Args:
        playlist: The playlist to build the rss file for.

    Returns:
        The path to the rss file.
    """
    feed = PlaylistFeedGenerator(playlist=playlist)
    rss_file = await feed.save()
    return rss_file