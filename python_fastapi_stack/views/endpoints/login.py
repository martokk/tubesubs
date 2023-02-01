from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from python_fastapi_stack.api.deps import get_db
from python_fastapi_stack.core import security

router = APIRouter()
templates = Jinja2Templates(directory="python_fastapi_stack/views/templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> Response:
    """
    Login Page.

    Args:
        request(Request): The request object

    Returns:
        Response: Login page

    """
    return templates.TemplateResponse("login/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def handle_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Response:
    """
    Handle login.

    Args:
        request(Request): The request object
        form_data(OAuth2PasswordRequestForm): The form data (username and password)
        db(Session): The database session.

    Returns:
        Response: Redirect to home page after login
    """
    try:
        tokens = await security.login_access_token(db=db, form_data=form_data)
    except HTTPException as e:
        return templates.TemplateResponse("login/login.html", {"request": request, "error": e})

    # Set the cookie
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {tokens['access_token']}", httponly=True)

    return response


@router.get("/logout", response_class=HTMLResponse)
async def logout(response: Response) -> Response:
    """
    Logout user by deleting the cookie.

    Args:
        response(Response): The response object

    Returns:
        Response: Redirect to home page after logout
    """
    response.delete_cookie("access_token")
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/"
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(
    request: Request,
) -> Response:
    """
    TODO: Registration page

    Args:
        request(Request): The request object

    Returns:
        Response: Registration page
    """
    return RedirectResponse(url="/login")
