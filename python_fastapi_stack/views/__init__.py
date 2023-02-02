from fastapi.templating import Jinja2Templates
from python_fastapi_stack import settings, paths

# Create Jinja2Templates object
templates = Jinja2Templates(directory=paths.TEMPLATES_PATH)

# Add global variables to templates
templates.env.globals["PROJECT_NAME"] = settings.PROJECT_NAME
templates.env.globals["PROJECT_DESCRIPTION"] = settings.PROJECT_DESCRIPTION
