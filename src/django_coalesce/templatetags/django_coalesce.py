from django import template
from django.db import models

register = template.Library()


@register.filter
def to_python_type(field: models.Field) -> str:
    match field:
        case models.IntegerField():
            return "int"
        case models.CharField():
            return "str"
    raise ValueError(f"{type(field)} is not yet supported")


@register.filter
def to_typescript_type(field: models.Field) -> str:
    match field:
        case models.IntegerField():
            return "number"
        case models.CharField():
            return "string"
    raise ValueError(f"{type(field)} is not yet supported")


@register.simple_tag
def literal(string: str) -> str:
    return string


@register.filter
def split(string: str, sep: str) -> list[str]:
    return string.split(sep)
