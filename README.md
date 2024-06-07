# django-coalesce

[![PyPI version](https://badge.fury.io/py/django-coalesce.svg)](https://badge.fury.io/py/django-coalesce)

What makes the world's most powerful batteries-included web framework even better? Automatically generating more batteries! 🔋

Inspired by the awesome .NET [Coalesce](https://intellitect.github.io/Coalesce/) project for accelerated web app development.

## Features

### Generate [Django Ninja](https://django-ninja.dev/) API CRUD views — WIP

Given the following Django model:
```python
# models.py
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField()
```

<details>
<summary>Generates the following Django Ninja module:</summary>

```python
# user_api.g.py
from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from blog.models import User


router = Router()


class UserIn(Schema):
    email: str


class UserOut(Schema):
    id: int
    email: str


@router.post("/", response=UserOut)
def create_user(request, payload: UserIn):
    user = User.objects.create(**payload.dict())
    return {"id": user.id}


@router.get("/{user_id}/", response=UserOut)
def get_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return user


@router.get("/", response=list[UserOut])
def list_users(request):
    users = User.objects.all()
    return users


@router.put("/{user_id}/")
def update_user(request, user_id: int, payload: UserIn):
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return {"success": True}


@router.delete("/{user_id}/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return {"success": True}
```

</details>

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
