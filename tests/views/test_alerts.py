from unittest.mock import Mock
from python_fastapi_stack import models
from fastapi import Request


def test_set_alerts_from_request(request: Request) -> None:
    """
    Test setting alerts from request (cookies)
    """
    # Mock the request
    request = Mock()
    request.cookies = {"alerts": '{"primary": ["Primary Alert"], "secondary": ["Secondary Alert"]}'}

    alerts = models.Alerts().from_request(request=request)
    assert alerts.primary == ["Primary Alert"]
    assert alerts.secondary == ["Secondary Alert"]
