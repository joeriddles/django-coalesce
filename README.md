# django-coalesce

Inspired by the awesome .NET [Coalesce](https://intellitect.github.io/Coalesce/) project for accelerated web app development.

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
