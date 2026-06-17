import os
import pathlib as p
import tempfile

import platformdirs
import pydantic as pd
from rich.markup import escape as _esc
from rich.markup import render as _render

from .. import error
from .._meta import AUTHOR
from .._pydantic_base import BM_Frozen


def get_default_database_dir() -> p.Path:
	"""Using platformdirs module, get a user data directory for this application, ensuring it exists.

	Returns:
		path: A pathlib.Path object representing the user data directory for this application.
	"""

	return p.Path(
		platformdirs.user_data_dir(
			appname=__package__.split(".")[0],
			appauthor=AUTHOR,
			ensure_exists=True,
		)
	)


class AppConfigurationError(error.RbDisplayError):
	"""Raised when the `App` instance is fatally misconfigured on `.run()`."""


class App(BM_Frozen):
	TOKEN: str = pd.Field(kw_only=False)
	"""Discord authentication token"""

	DATABASE_DIR: p.Path = pd.Field(default_factory=get_default_database_dir)
	"""Path to an existing directory to store the sqlite db files in."""

	@pd.model_validator(mode="after")
	def _(self) -> None:
		if not self.TOKEN:
			msg = "TOKEN is an empty string."
			raise AppConfigurationError(msg)

		if not (self.DATABASE_DIR.is_dir() and _empirical_path_check_rwx_access(self.DATABASE_DIR)):
			msg = _render(
				f"DATABASE_DIR is not a [red b]valid[/] path to an [red b]existing[/], [red b]rwx[/] directory: [red b u]{_esc(str(self.DATABASE_DIR))}[/]"
			)
			raise AppConfigurationError(msg)

	def run(self) -> None:
		pass


if True:  # helper functions

	def _empirical_path_check_rwx_access(path: p.Path) -> bool:
		try:
			with tempfile.TemporaryFile(dir=path):
				pass
		except OSError, PermissionError:
			return False

		return True
