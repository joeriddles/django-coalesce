# import ast
import dataclasses
import inspect
import os
import pathlib
import types
from typing import Generator, Protocol, Type

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
            for _, type_ in inspect.getmembers(
                module, self._filter_concrete_django_models
            )
        ]

    def _filter_concrete_django_models(self, m) -> bool:
        return inspect.isclass(m) and issubclass(m, Model) and not m._meta.abstract


class BaseGenerator(Protocol):
    def generate(self, model_info: ModelInfo) -> str: ...


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


def write(filepath: str | pathlib.Path, content: str) -> None:
    with open(filepath, "w") as fout:
        fout.write(content)


def main(module: types.ModuleType) -> Generator[str, None, None]:
    model_infos = Finder().find(module)
    parent_module_name = module.__name__.rsplit(".", maxsplit=1)[0]

    for model_info in model_infos:
        module_folder_path: str = pathlib.Path(module.__file__).parent  # type: ignore
        generated_folder_path = pathlib.Path(module_folder_path, "generated")

        try:
            os.mkdir(generated_folder_path)
        except FileExistsError:
            pass

        content = TypescriptModelGenerator().generate(model_info)
        filename = f"{model_info.model_name.casefold()}.g.ts"
        write(generated_folder_path / filename, content)
        yield f"{parent_module_name}.generated.{filename}"

        content = DjangoNinjaCrudGenerator().generate(model_info)
        filename = f"{model_info.model_name.casefold()}_api.g.py"
        write(generated_folder_path / filename, content)
        yield f"{parent_module_name}.generated.{filename}"

        content = ""
        filename = "__init__.py"
        write(generated_folder_path / filename, content)
        yield f"{parent_module_name}.generated.{filename}"
