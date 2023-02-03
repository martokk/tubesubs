from sqlmodel import Session

from python_fastapi_stack import models
from python_fastapi_stack.views import deps


async def test_get_db() -> None:
    """
    Test get_db() dependency.
    """
    db = next(deps.get_db())
    assert isinstance(db, Session)
