from loguru import logger as _logger

from python_fastapi_stack import settings
from python_fastapi_stack.paths import LOG_FILE

_logger.add(LOG_FILE, level=settings.LOG_LEVEL, rotation="10 MB")
_logger.info(f"Log level set by .env to '{settings.LOG_LEVEL}'")

logger = _logger
