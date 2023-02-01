from unittest.mock import patch

from fastapi import Request
from fastapi.testclient import TestClient
from sqlmodel import Session

from python_fastapi_stack import settings

# from python_fastapi_stack.views.endpoints.items import html_view_items
from tests.mock_objects import MOCKED_ITEMS

# async def test_html_view_items(
#     db_with_user: Session,
#     test_request: Request,
#     client: TestClient,
#     superuser_token_headers: dict[str, str],
# ) -> None:
#     """
#     Test that the html_view_items function returns a response with the correct status code.
#     """
#     # Create 3 items
#     for item in MOCKED_ITEMS:
#         response = client.post(
#             f"{settings.API_V1_PREFIX}/item/",
#             headers=superuser_token_headers,
#             json=item,
#         )
#         assert response.status_code == 201

#     # Mock the TemplateResponse
#     with patch(
#         "python_fastapi_stack.views.endpoints.item.templates.TemplateResponse"
#     ) as mock_template_response:
#         await html_view_items(
#             request=test_request,
#             db=db_with_user,
#         )

#         assert mock_template_response.called

#         # Test that the correct arguments are passed to the TemplateResponse
#         assert mock_template_response.call_args[0][0] == "view_items.html"

#         response_context = mock_template_response.call_args[0][1]
#         assert response_context["request"] == test_request
#         assert len(response_context["items"]) == 3
