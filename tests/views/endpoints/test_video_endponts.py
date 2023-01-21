from unittest.mock import patch

from fastapi import Request
from sqlmodel import Session

from python_fastapi_stack.views.endpoints.videos import html_view_videos


async def test_html_view_videos(db_with_videos: Session, test_request: Request) -> None:
    """
    Test that the html_view_videos function returns a response with the correct status code.
    """
    with patch(
        "python_fastapi_stack.views.endpoints.videos.templates.TemplateResponse"
    ) as mock_template_response:
        await html_view_videos(
            request=test_request,
            db=db_with_videos,
        )

        assert mock_template_response.called

        # Test that the correct arguments are passed to the TemplateResponse
        assert mock_template_response.call_args[0][0] == "view_videos.html"

        response_context = mock_template_response.call_args[0][1]
        assert response_context["request"] == test_request
        assert len(response_context["videos"]) == 3
