from __future__ import annotations

import contextlib
import os
from typing import Generator, Iterable, Self, overload


class CodeBuilder:
    """
    A string builder that simplifies the process of building code.
    Contains operations common to the process of constructing chunks of code,
    fully supporting customizable indentation.
    """

    @property
    def level(self) -> int:
        return self._level

    def __init__(
        self,
        initial_level: int = 0,
        indent_size: int = 4,
        indent_char: str = " ",
    ):
        self._level = initial_level
        self._indent_size = indent_size
        self._indent_char = indent_char
        self._on_new_line: bool = False
        self._sb = ""  # TODO: port StringBuilder class from .NET ?

    def __str__(self) -> str:
        return self._sb

    @overload
    def line(self) -> Self:
        """Write a blank line at the current indentation level."""
        ...

    @overload
    def line(self, line: str) -> Self:
        """
        Write a line of text at the current indentation level.
        If `append(string)` was called previously, no indentation will be added.
        """

    def line(self, line: str = "") -> Self:
        if self._on_new_line:
            self._sb += self._indent_char * (self.level * self._indent_size)
        self._sb += line + os.linesep
        self._on_new_line = True
        return self

    def lines(self, lines: Iterable[str]) -> Self:
        """Calls `line(string)` for each line."""
        for line in lines:
            self.line(line)
        return self

    @overload
    def indented(self, line: str) -> Self:
        """
        Write a line that is indented one level past the current indentation level.

        Raises:
            ValueError: Not currently at the start of a blank line - cannot add
            indented text at the current location.
        """
        ...

    @overload
    def indented(self) -> contextlib._GeneratorContextManager:
        """
        Increases indentation one level, returning an context manager that
        decreases indentation when exited.
        """
        ...

    def indented(self, line: str | None = None):
        """
        Write a line that is indented one level past the current indentation level.

        Raises:
            ValueError: Not currently at the start of a blank line - cannot add
            indented text at the current location.
        """
        if line:
            if self._on_new_line:
                self._sb += self._indent_char * ((self.level + 1) * self._indent_size)
            else:
                raise ValueError(
                    "Cannot start an indented line on a line that isn't empty."
                )
            self._sb += line + os.linesep
            self._on_new_line = True
            return self
        else:
            self._level += 1
            return self.Indentation(self)

    def append(self, text: str) -> Self:
        """
        Write text to the current line. If currently on a new, blank line, the
        current indentation will be added.
        """
        if self._on_new_line:
            self._sb += self._indent_char * (self.level * self._indent_size)
            self._on_new_line = False
        self._sb += text
        return self

    def trim_end(self, text: str) -> Self:
        """Trim the given string from the end of the output if it exists."""
        if self._sb[len(self._sb) - len(text) :] == text:
            self._sb = self._sb[: len(self._sb) - len(text)]
        return self

    def trim_whitespace(self) -> Self:
        """Trim whitespace from the end of the output."""
        self._sb = self._sb.rstrip()
        return self

    @staticmethod
    @contextlib.contextmanager
    def Indentation(
        parent: CodeBuilder,
        close_with: str | None = None,
    ) -> Generator[None, None, None]:
        try:
            yield
        finally:
            parent._level -= 1
            if close_with is not None:
                parent.line(close_with)
