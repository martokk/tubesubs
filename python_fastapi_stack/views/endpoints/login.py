import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlmodel import Session

from python_fastapi_stack import logger, models, settings
from python_fastapi_stack.api.deps import get_db
from python_fastapi_stack.core import security
from python_fastapi_stack.views import templates

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, success: bool | None = None) -> Response:
    """
    Login Page.

    Args:
        request(Request): The request object
        success(bool): Whether the user was created successfully

    Returns:
        Response: Login page

    """
    alerts = models.Alerts()
    if success:
        alerts.success.append("User created successfully")
    return templates.TemplateResponse("login/login.html", {"request": request, "alerts": alerts})


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
        tokens = await security.get_tokens_from_username_password(db=db, form_data=form_data)
    except HTTPException as e:
        return templates.TemplateResponse("login/login.html", {"request": request, "error": e})

    # Set the cookie
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {tokens.access_token}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"Bearer {tokens.refresh_token}", httponly=True)

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
    response.delete_cookie("refresh_token")
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/"
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(
    request: Request,
) -> Response:
    """
    Args:
        request(Request): The request object

    Returns:
        Response: Registration page
    """

    return templates.TemplateResponse(
        "login/register.html",
        {"request": request, "registration_enabled": settings.USERS_OPEN_REGISTRATION},
    )


@router.post("/register", response_class=HTMLResponse)
async def handle_registration(
    request: Request,
    username: str = Form(None),
    password: str = Form(None),
    password_confirmation: str = Form(None),
    email: str = Form(None),
    full_name: str = Form(None),
) -> Response:
    """
    Handle registration.
    # TODO: Add captcha

    Args:
        request(Request): The request object
        username(str): The username
        password(str): The password
        password_confirmation(str): The password confirmation
        email(str): The email
        full_name(str): The full name

    Returns:
        Response: Registration page

    Raises:
        HTTPException: Registration is disabled
    """
    alerts = models.Alerts()
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Registration is disabled"
        )

    # Check if all fields are filled
    if not all([username, password, password_confirmation, email, full_name]):
        alerts.danger.append("Please fill out all fields")

    # Confirm passwords match
    if password != password_confirmation:
        alerts.danger.append("Passwords do not match")

    # Validate email via pydantic
    valid_email = None
    try:
        valid_email = EmailStr.validate(email)
    except ValueError:
        alerts.danger.append("Invalid email")

    # Post to the API if there are no errors
    if not alerts.danger:
        endpoint = f"{settings.BASE_URL}{settings.API_V1_PREFIX}/register"
        data = {
            "username": username,
            "password": password,
            "email": valid_email,
            "full_name": full_name,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url=endpoint, json=data, timeout=2)

        # Handle response
        if response.status_code == status.HTTP_201_CREATED:
            return RedirectResponse("/login?success=true", status_code=status.HTTP_302_FOUND)
        elif response.status_code == status.HTTP_409_CONFLICT:
            alerts.danger.append("Username or email already exists")
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            alerts.danger.append("Invalid data")
            logger.error(f"Error registering user: {response.status_code=}, {response.text=}")
        else:
            logger.error(f"Error registering user: {response.status_code=}, {response.text=}")
            alerts.danger.append("Error registering user")

    # Return the registration page with alert messages
    return templates.TemplateResponse(
        "login/register.html",
        {
            "request": request,
            "registration_enabled": settings.USERS_OPEN_REGISTRATION,
            "alerts": alerts,
        },
    )
