from app import models

from .base import BaseCRUD


class FilterGroupCRUD(
    BaseCRUD[models.FilterGroup, models.FilterGroupCreate, models.FilterGroupUpdate]
):
    ...


filter_group = FilterGroupCRUD(model=models.FilterGroup)
