from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from sqlmodel import Session

from app import crud, logger, settings, version
from app.api import deps
from app.api.v1.api import api_router
from app.core import notify
from app.db.init_db import init_initial_data
from app.paths import STATIC_PATH
from app.services.fetch import fetch_all_subscriptions
from app.views.router import views_router

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=version,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    debug=settings.DEBUG,
)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(views_router)

# STATIC_PATH.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_PATH))


@app.on_event("startup")  # type: ignore
async def on_startup(db: Session = next(deps.get_db())) -> None:
    """
    Event handler that gets called when the application starts.
    Logs application start and creates database and tables if they do not exist.

    Args:
        db (Session): Database session.
    """
    logger.info("--- Start FastAPI ---")
    logger.debug("Starting FastAPI App...")
    if settings.NOTIFY_ON_START:
        await notify.notify(text=f"{settings.PROJECT_NAME}('{settings.ENV_NAME}') started.")

    await init_initial_data(db=db)


@app.on_event("startup")  # type: ignore
@repeat_every(seconds=settings.REFRESH_SUBSCRIPTIONS_INTERVAL_MINUTES * 60, wait_first=True)
async def repeating_fetch_all_sources() -> None:  # pragma: no cover
    """
    Fetches all Sources from yt-dlp.
    """
    logger.debug("Repeating fetch of All Subscriptions...")
    db: Session = next(deps.get_db())
    fetch_results = await fetch_all_subscriptions(db=db)
    logger.success(f"Completed refreshing {fetch_results.subscriptions} Subscriptions from yt-dlp.")


# @app.on_event("startup")  # type: ignore
# async def delete_long_videos() -> None:  # pragma: no cover
#     """
#     Fetches all Sources from yt-dlp.
#     """
#     logger.debug("Deleting Long Videos")
#     db: Session = next(deps.get_db())

#     videos = await crud.video.get_all(db=db)

#     deleted_count = 0
#     for video in videos:
#         if video.duration and video.duration > 6300:
#             print(f"dur={video.duration} title={video.title}")
#             await crud.video.remove(db=db, id=video.id)
#             deleted_count += 1

#     logger.success(f"Completed deleting {deleted_count} Long Videos")
