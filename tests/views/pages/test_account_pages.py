import pytest
from fastapi.testclient import TestClient
from httpx import Cookies
from sqlmodel import Session

from tests.mock_objects import MOCKED_ITEM_1, MOCKED_ITEMS
