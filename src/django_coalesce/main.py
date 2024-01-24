# import ast
import dataclasses
import inspect
import types
from typing import Protocol, Type

from django.conf import settings
from django.db.models import Model
from django.template import loader


@dataclasses.dataclass
class ModelInfo:
    model_class: Type[Model]

    @property
    def meta(self):
        return self.model_class._meta

    @property
    def model_name(self) -> str:
        if not self.model_class._meta.model_name:
            raise TypeError("model_class._meta.model_name is None")
        return self.model_class._meta.model_name

    @property
    def fields(self):
        return self.model_class._meta.get_fields()


class Finder:
    """Find Django model classes"""

    def find(self, module: types.ModuleType) -> list[ModelInfo]:
        return [
            ModelInfo(type_)
            for _, type_ in inspect.getmembers(module, self._filter_django_models)
        ]

    def _filter_django_models(self, m) -> bool:
        return inspect.isclass(m) and issubclass(m, Model)


class BaseGenerator(Protocol):
    def generate(self, model_info: ModelInfo) -> str:
        ...


class TypescriptModelGenerator(BaseGenerator):
    def generate(self, model_info: ModelInfo):
        content = loader.render_to_string(
            "django_coalesce/model.ts",
            {"model": model_info},
        )
        return content


class DjangoNinjaCrudGenerator(BaseGenerator):
    def generate(self, model_info: ModelInfo):
        content = loader.render_to_string(
            "django_coalesce/api.py",
            {"model": model_info},
        )
        return content


def main(module: types.ModuleType):
    model_infos = Finder().find(module)
    for model_info in model_infos:
        content = TypescriptModelGenerator().generate(model_info)
        filename = f"{model_info.model_name.casefold()}.g.ts"
        with open(settings.BASE_DIR.parent / "generated" / filename, "w") as fout:
            fout.write(content)

        content = DjangoNinjaCrudGenerator().generate(model_info)
        filename = f"{model_info.model_name.casefold()}_api.g.py"
        with open(settings.BASE_DIR.parent / "generated" / filename, "w") as fout:
            fout.write(content)
