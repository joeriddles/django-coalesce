from django_coalesce.builders import CodeBuilder


def test__code_builder__line():
    builder = CodeBuilder()
    builder.line()
    actual = str(builder)
    expected = "\n"
    assert actual == expected


def test__code_builder__line__with_str():
    builder = CodeBuilder()
    builder.line("print('hello world')")
    actual = str(builder)
    expected = "print('hello world')\n"
    assert actual == expected


def test__code_builder__lines():
    builder = CodeBuilder()
    builder.lines(["print('hello world')", "print('another line')"])
    actual = str(builder)
    expected = "print('hello world')\nprint('another line')\n"
    assert actual == expected


def test__code_builder__indented__with_str():
    builder = CodeBuilder()
    builder.line("if True:")
    builder.indented("print('hello world')")
    actual = str(builder)
    # fmt: off
    expected = (
        "if True:\n"
        "    print('hello world')\n"
    )
    # fmt: on
    assert actual == expected


def test__code_builder__indented():
    builder = CodeBuilder()
    builder.line("if True:")
    with builder.indented():
        builder.line("print('hello world')")

    actual = str(builder)
    # fmt: off
    expected = (
        "if True:\n"
        "    print('hello world')\n"
    )
    # fmt: on
    assert actual == expected


def test__code_builder__append():
    builder = CodeBuilder()
    builder.append("print(")
    builder.append("'hello world'")
    builder.append(")")
    builder.line()
    actual = str(builder)
    expected = "print('hello world')\n"
    assert actual == expected


def test__code_builder__append__when_indented():
    builder = CodeBuilder()
    builder.line("if True:")
    with builder.indented():
        builder.append("print(")
        builder.append("'hello world'")
        builder.append(")")
    builder.line()
    actual = str(builder)
    # fmt: off
    expected = (
        "if True:\n"
        "    print('hello world')\n"
    )
    # fmt: on
    assert actual == expected


def test__code_builder__trim_end__matches():
    builder = CodeBuilder()
    builder.line("print('hello world')")
    builder.trim_end(" world')\n")
    builder.append("')\n")
    actual = str(builder)
    expected = "print('hello')\n"
    assert actual == expected


def test__code_builder__trim_end__no_match():
    builder = CodeBuilder()
    builder.line("print('hello world')")
    builder.trim_end("NO MATCH")
    actual = str(builder)
    expected = "print('hello world')\n"
    assert actual == expected


def test__code_builder__trim_whitespace__matches():
    builder = CodeBuilder()
    builder.line("print('hello world')    ")
    builder.trim_whitespace()
    actual = str(builder)
    expected = "print('hello world')"  # removes newline
    assert actual == expected


def test__code_builder__trim_whitespace__no_match():
    builder = CodeBuilder()
    builder.append("print('hello world')")
    builder.trim_whitespace()
    actual = str(builder)
    expected = "print('hello world')"
    assert actual == expected
