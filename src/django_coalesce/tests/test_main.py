from django.conf import settings

from django_coalesce import main, models


def test_main_user():
    main.main(models)
    expected = """export interface user {
    id: number;
    email: string;
}
"""
    with open(settings.BASE_DIR.parent / "generated" / "user.g.ts") as fin:
        actual = fin.read()
    assert actual == expected
