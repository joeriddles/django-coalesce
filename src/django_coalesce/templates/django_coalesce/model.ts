{% load django_coalesce %}{% include "django_coalesce/partials/header.txt" %}

export interface {{ model.model_name }} {
    {% spaceless %}
    {% for field in model.fields %}{{ field.name }}: {{ field|to_typescript_type }};
    {% endfor %}
    {% endspaceless %}
}
