from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlmodel import Session

from app import crud, models
from app.services.feed import build_rss_file
from app.views import deps, templates

router = APIRouter()


@router.post(
    "/filter/{filter_id}/criteria/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def handle_create_criteria(
    filter_id: str,
    field: str = Form(...),
    operator: str = Form(...),
    value: str = Form(...),
    unit_of_measure: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new Criteria.

    Args:
        filter_id(str): The filter id
        id(str): The criteria id
        field(str): The field of the criteria
        operator(str): The operator of the criteria
        value(str): The value of the criteria
        unit_of_measure(str): The unit of measure of the criteria
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of filters view
    """
    alerts = models.Alerts()

    try:
        obj_in = models.CriteriaCreate(
            filter_id=filter_id,
            field=field,
            operator=operator,
            value=value,
            unit_of_measure=unit_of_measure,
        )
    except ValidationError as exc:
        alerts.danger.append(str(exc.args[0][0].exc.args[0]))
        response = RedirectResponse(f"/filter/{filter_id}/edit", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    try:
        await crud.criteria.create(db=db, obj_in=obj_in)
    except ValueError as exc:
        alerts.danger.append(str(exc.args[0]))
        response = RedirectResponse(f"/filter/{filter_id}/edit", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    alerts.success.append("Criteria successfully created.")
    response = RedirectResponse(
        url=f"/filter/{filter_id}/edit", status_code=status.HTTP_303_SEE_OTHER
    )
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter/{filter_id}/criteria/{id}/edit", response_class=HTMLResponse)
async def edit_criteria(
    request: Request,
    filter_id: str,
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit Criteria form.

    Args:
        request(Request): The request object
        filter_id(str): The filter id
        id(str): The criteria id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new filter
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        criteria = await crud.criteria.get(db=db, id=id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Criteria not found")
        response = RedirectResponse(f"/filter/{filter_id}", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Build Criterias Options
    options_criteria_fields = list(attr.value for attr in models.CriteriaField)
    options_created_at_operators = [
        models.CriteriaOperator.WITHIN.value,
        models.CriteriaOperator.AFTER.value,
    ]
    options_duration_operators = [
        models.CriteriaOperator.SHORTER_THAN.value,
        models.CriteriaOperator.LONGER_THAN.value,
    ]
    options_keyword_operators = [
        models.CriteriaOperator.MUST_CONTAIN.value,
        models.CriteriaOperator.MUST_NOT_CONTAIN.value,
    ]
    options_read_status_operators = [
        models.CriteriaOperator.IS.value,
    ]
    options_channel_id_operators = [
        models.CriteriaOperator.IS.value,
        models.CriteriaOperator.IS_NOT.value,
    ]
    options_channel_operators = [
        models.CriteriaOperator.MUST_CONTAIN.value,
        models.CriteriaOperator.MUST_NOT_CONTAIN.value,
    ]
    options_priority_operators = [
        models.CriteriaOperator.LESS_THAN.value,
        models.CriteriaOperator.EQUAL_TO.value,
        models.CriteriaOperator.GREATER_THAN.value,
    ]

    options_read_status_values = [
        models.CriteriaValue.UNREAD.value,
        models.CriteriaValue.READ.value,
    ]

    all_tags = await crud.tag.get_all(db=db)
    options_tag_values = [tag.name for tag in all_tags]
    options_tag_values.append("ANY")

    return templates.TemplateResponse(
        "criteria/edit.html",
        {
            "request": request,
            "criteria": criteria,
            "current_user": current_user,
            "alerts": alerts,
            "options_criteria_fields": options_criteria_fields,
            "options_created_at_operators": options_created_at_operators,
            "options_duration_operators": options_duration_operators,
            "options_keyword_operators": options_keyword_operators,
            "options_read_status_operators": options_read_status_operators,
            "options_channel_id_operators": options_channel_id_operators,
            "options_channel_operators": options_channel_operators,
            "options_priority_operators": options_priority_operators,
            "options_read_status_values": options_read_status_values,
            "options_tag_values": options_tag_values,
        },
    )


@router.post("/filter/{filter_id}/criteria/{id}/edit", response_class=HTMLResponse)
async def handle_edit_criteria(
    request: Request,
    filter_id: str,
    id: str,
    field: str = Form(...),
    operator: str = Form(...),
    value: str = Form(...),
    unit_of_measure: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles editing of a criteria.

    Args:
        request(Request): The request object
        filter_id(str): The filter id
        id(str): The criteria id
        field(str): The field of the criteria
        operator(str): The operator of the criteria
        value(str): The value of the criteria
        unit_of_measure(str): The unit of measure of the criteria
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Filter view with updated criteria
    """
    alerts = models.Alerts()
    criteria_update = models.CriteriaUpdate(
        field=field, operator=operator, value=value, unit_of_measure=unit_of_measure
    )

    try:
        new_criteria = await crud.criteria.update(db=db, obj_in=criteria_update, id=id)
        alerts.success.append(f"Criteria '{new_criteria.name}' updated")
    except ValueError as exc:
        alerts.danger.append(str(exc.args[0]))
        response = RedirectResponse(f"/filter/{filter_id}", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    except crud.RecordNotFoundError:
        alerts.danger.append("Criteria not found")

    response = RedirectResponse(
        url=f"/filter/{filter_id}/edit", status_code=status.HTTP_303_SEE_OTHER
    )
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter/{filter_id}/criteria/{id}/delete", response_class=HTMLResponse)
async def delete_criteria(
    filter_id: str,
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete a criteria.

    Args:
        filter_id(str): The filter id
        id(str): The criteria id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Filter view with updated criteria
    """
    alerts = models.Alerts()
    try:
        await crud.criteria.remove(db=db, id=id, filter_id=filter_id)
        alerts.success.append("Criteria deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Criteria not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting criteria")

    response = RedirectResponse(
        url=f"/filter/{filter_id}/edit", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
