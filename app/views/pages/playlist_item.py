from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.views import deps

router = APIRouter()


@router.get(
    "/playlist/{playlist_id}/playlist_item/{playlist_item_id}/delete", response_class=HTMLResponse
)
async def delete_playlist_item(
    playlist_id: str,
    playlist_item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete Playlist Item view.

    Args:
        playlist_id(str): The playlist id
        playlist_item_id(str): The playlist_item_id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to delete a new playlist
    """
    alerts = models.Alerts()
    try:
        await crud.playlist_item.remove(db=db, id=playlist_item_id, playlist_id=playlist_id)
        alerts.success.append("Playlist Item deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Playlist Item not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting playlist Item")

    response = RedirectResponse(
        url=f"/playlist/{playlist_id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
