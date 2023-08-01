# PROJECT STRUCTURE
import os
from pathlib import Path

# Project Path
BASE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))

# Folders
DATA_PATH = BASE_PATH / "data"
VIEWS_PATH = BASE_PATH / "views"

# Views Folder
STATIC_PATH = VIEWS_PATH / "static"
EMAIL_TEMPLATES_PATH = VIEWS_PATH / "email-templates" / "src"
TEMPLATES_PATH = VIEWS_PATH / "templates"

# Data Folder
LOGS_PATH = DATA_PATH / "logs"
CACHE_PATH = DATA_PATH / "cache"
COOKIES_PATH = DATA_PATH / "cookies"
FEEDS_PATH = DATA_PATH / "feed"

# COOKIE FILES
YOUTUBE_COOKIES_FILE = COOKIES_PATH / "youtube_cookies.txt"

# Files
ENV_FILE = DATA_PATH / ".env"
DATABASE_FILE = DATA_PATH / "database.sqlite3"
LOG_FILE = LOGS_PATH / "log.log"
ERROR_LOG_FILE = LOGS_PATH / "error_log.log"
