import importlib

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_coalesce import main


class Command(BaseCommand):
    help = "Generate code"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        app_configs = apps.get_app_configs()
        project_name = settings.COALESCE_PROJECT_NAME

        for app_config in app_configs:
            if app_config.name.startswith(f"{project_name}.") and (
                models_module := app_config.models_module
            ):
                if isinstance(models_module, str):
                    models_module = importlib.import_module(models_module)
                main.main(models_module)

        # raise CommandError('Poll "%s" does not exist' % poll_id)
        # self.stdout.write(
        #     self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
        # )
