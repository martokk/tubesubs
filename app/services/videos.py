from sqlmodel import Session
from app import crud, models


async def mark_videos_as_read(db: Session, video_ids: list[str]) -> None:
    for video_id in video_ids:
        await crud.video.update(
            db=db, id=video_id, obj_in=models.VideoUpdate(id=video_id, is_read=True)
        )
