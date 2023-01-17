from fastapi import APIRouter, Depends, status
from pydantic.networks import EmailStr

from python_fastapi_stack import models
from python_fastapi_stack.api import deps
from python_fastapi_stack.core import notify

router = APIRouter()


# @router.post("/test-celery/", response_model=models.Msg, status_code=status.HTTP_201_CREATED)
# def test_celery(
#     msg: models.Msg,
#     _: models.User = Depends(deps.get_current_active_superuser),
# ) -> dict[str, str]:
#     """
#     Test Celery worker.

#     Args:
#         msg (schemas.Msg): The message to send to the worker.
#         _: models.User: The current user.

#     Returns:
#         dict[str, str]: A dictionary with the message.
#     """
#     celery_app.send_task("app.worker.test_celery", args=[msg.msg])
#     return {"msg": "Word received"}


@router.post("/test-email/", response_model=models.Msg, status_code=status.HTTP_201_CREATED)
def test_email(
    email_to: EmailStr,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> dict[str, str]:
    """
    Test emails.

    Args:
        email_to (EmailStr): The email to send the test to.

    Returns:
        dict[str, str]: A dictionary with the message.
    """
    notify.send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
