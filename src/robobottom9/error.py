from dataclasses import dataclass as _dataclass
from dataclasses import field as _field

from rich.markup import escape as _esc
from rich.markup import render as _render
from rich.text import Text as _Text


class RbError(Exception):
	"""Base class for all custom errors raised by this project."""


@_dataclass
class RbDisplayError(RbError):
	"""Base class for all errors that should be displayed to the user instead of raising a stack trace."""

	text: str | _Text
	"""The visible text to display to the user, if str, will be converted to a simple non-highlighted Text derived from said str."""

	exitcode: int = _field(default=1, kw_only=True)
	"""The exit code to use when exiting the program due to this error, if 0 and the bot has successfully started (can fall back to simply waiting for events, and discarding this one) don't exit, if exiting is necessary (like when the bot hasn't started properly and this is set to 0, exit with exit code of 1)."""

	def __rich__(self) -> _Text:
		if isinstance(self.text, str):
			self.text = _Text(self.text)

		return _render(f"[red b]{_esc(self.__class__.__name__)}:[/] ") + self.text
