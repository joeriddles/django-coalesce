# django-coalesce

[![PyPI version](https://badge.fury.io/py/django-coalesce.svg)](https://badge.fury.io/py/django-coalesce)

Inspired by the awesome .NET [Coalesce](https://intellitect.github.io/Coalesce/) project for accelerated web app development.

## Features

### Generate TypeScript models from Django models — WIP

Given the following Django model:
```python
# models.py
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField()
```

Generates the following TypeScript model:
```typescript
// user.g.ts
export interface user {
    id: number;
    email: string;
}
```

## Development

### Getting Started

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev.txt

# not required but makes setting PYTHONPATH and DJANGO_SETTINGS_MODULE easier
direnv allow
```

### Build

```shell
python3 -m pip install --upgrade build twine
python3 -m build
```

Upload to [test.pypi.org](https://test.pypi.org)

```shell
python3 -m twine upload --repository testpypi dist/*
```

Upload to [PyPI](https://pypi.org)

```shell
python3 -m twine upload dist/*
```
