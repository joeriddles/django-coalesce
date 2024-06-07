{% load django_coalesce %}{% include "django_coalesce/partials/header.txt" %}{% with ObjectName=model.meta.object_name %}{% with model_name=model.model_name %}
from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from {{ model.meta.app_label }}.models import {{ model.meta.label|split:"."|last }}


router = Router()


class {{ ObjectName }}In(Schema):
    {% spaceless %}
    {% for field in model.fields %}
    {% if not field.primary_key %}
    {{ field.name }}: {{ field|to_python_type }}
    {% endif %}
    {% endfor %}
    {% endspaceless %}


class {{ ObjectName }}Out(Schema):
    {% spaceless %}
    {% for field in model.fields %}{{ field.name }}: {{ field|to_python_type }}
    {% endfor %}
    {% endspaceless %}


@router.post("/", response={{ ObjectName }}Out)
def create_{{ model_name }}(request, payload: {{ ObjectName }}In):
    {{ model_name }} = {{ ObjectName }}.objects.create(**payload.dict())
    return {"{{ model.meta.pk.name }}": {{ model_name }}.{{ model.meta.pk.name }}}


@router.get("/{% literal '{' %}{{ model_name }}_{{ model.meta.pk.name }}{% literal '}' %}/", response={{ ObjectName }}Out)
def get_{{ model_name }}(request, {{ model_name }}_{{ model.meta.pk.name }}: int):
    {{ model_name }} = get_object_or_404({{ ObjectName }}, {{ model.meta.pk.name }}={{ model_name }}_{{ model.meta.pk.name }})
    return {{ model_name }}


@router.get("/", response=list[{{ ObjectName }}Out])
def list_{{ model_name }}s(request):
    {{ model_name }}s = {{ ObjectName }}.objects.all()
    return {{ model_name }}s


@router.put("/{% literal '{' %}{{ model_name }}_{{ model.meta.pk.name }}{% literal '}' %}/")
def update_{{ model_name }}(request, {{ model_name }}_{{ model.meta.pk.name }}: int, payload: {{ ObjectName }}In):
    {{ model_name }} = get_object_or_404({{ ObjectName }}, {{ model.meta.pk.name }}={{ model_name }}_{{ model.meta.pk.name }})
    for attr, value in payload.dict().items():
        setattr({{ model_name }}, attr, value)
    {{ model_name }}.save()
    return {"success": True}


@router.delete("/{% literal '{' %}{{ model_name }}_{{ model.meta.pk.name }}{% literal '}' %}/")
def delete_{{ model_name }}(request, {{ model_name }}_{{ model.meta.pk.name }}: int):
    {{ model_name }} = get_object_or_404({{ ObjectName }}, {{ model.meta.pk.name }}={{ model_name }}_{{ model.meta.pk.name }})
    {{ model_name }}.delete()
    return {"success": True}{% endwith %}{% endwith %}
