"""Minimal viable Django settings"""
from collections import OrderedDict
from pathlib import Path

from django.apps import AppConfig, apps

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(AppConfig):
    name = "config"


INSTALLED_APPS = [
    "django_coalesce.settings",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {
                "django_coalesce": "django_coalesce.templatetags.django_coalesce",
            }
        },
    },
]

apps.app_configs = OrderedDict()
apps.ready = False
apps.populate(INSTALLED_APPS)
