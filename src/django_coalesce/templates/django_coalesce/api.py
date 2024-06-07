{% load django_coalesce %}{% include "django_coalesce/partials/header.txt" %}
{% with ObjectName=model.meta.object_name %}{% with model_name=model.model_name %}
from django.apps import apps
from ninja import Router, Schema

{{ ObjectName }} = apps.get_model("{{ model.meta.app_label }}.{{ model.meta.model_name }}")


class {{ ObjectName }}Out(Schema):
    {% spaceless %}
    {% for field in model.fields %}{{ field.name }}: {{ field|to_python_type }}
    {% endfor %}
    {% endspaceless %}


router = Router()


@router.get("/", response=list[{{ ObjectName }}Out])
def list_{{ model_name }}s(request):
    {{ model_name }}s = {{ ObjectName }}.objects.all()
    return {{ model_name }}s
{% endwith %}{% endwith %}
