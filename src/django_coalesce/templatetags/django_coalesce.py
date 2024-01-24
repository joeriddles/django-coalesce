from django import template
from django.db import models

register = template.Library()


@register.filter
def to_typescript_type(field: models.Field) -> str:
    match field:
        case models.IntegerField():
            return "number"
        case models.CharField():
            return "string"
    raise ValueError(f"{type(field)} is not yet supported")
