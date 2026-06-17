import os
import pathlib as p
import sys

import arguably
import rich.traceback
from tcrutils.console import c
from tcrutils.string import get_token

from . import App, error
from . import __version__ as __version__


@arguably.command()
def __root__(
	token: str | None = None,
	*,
	tb_show_locals: bool = False,
) -> None:
	"""Command line interface for robobottom9.

	Args:
		token: Discord authentication token, if not provided try searching the environment variable `TOKEN`.
		tb_show_locals: [-L] Whether to show local variables in the rich.traceback.

	Raises:
		ValueError: If token is not provided via any of the ways to do so.
	"""  # noqa: DOC502 # disabled due to this rule being too dumb to notice assignment, and it is required for adding a note (add_note doesnt return self... damn i wish it just did!!!)

	if True:  # cli improvements
		try:
			terminal_width = os.get_terminal_size().columns
		except OSError:
			terminal_width = 100

		rich.traceback.install(
			width=terminal_width,
			show_locals=tb_show_locals,
			word_wrap=True,
		)

	if True:  # get token
		if token is None:
			token = os.environ.get("TOKEN")

		if token is None:
			token = get_token(default="") or None

		if token is None:
			msg = "No token provided via any of the ways to do so."

			note = """
Please provide a discord token via either one of:
1. First positional argument to this command.
2. Environment variable `TOKEN`
3. A file named `TOKEN.txt` in the current working directory or its parent directory.
"""[1:-1]

			err = ValueError(msg)
			err.add_note(note)
			raise err

	try:
		(
			c
			| App(
				TOKEN=token,
			)
		).run()
	except error.RbDisplayError as e:
		rich.print(e, file=sys.stderr)

		# as the docstring of error.RbDisplayError.exitcode states, if exitcode is set to 0, it means "try" to continue program execution, but at this point no way to continue, if this was in an event handler of some sorts then maybe, but here? nah. In such cases convert 0 to a 1
		sys.exit(e.exitcode or 1)


if True:  # helper functions

	def cli() -> None:
		"""The entry point to this `pyproject.toml`-defined script."""

		# fix for arguably to work, unfortunate bug i think, and this library is not getting maintained anymore.. :c
		sys.modules["__main__"].__version__ = __version__
		arguably.run(
			version_flag=("-V", "--version"),
			show_types=False,
			show_defaults=False,
		)

	def get_token[T](filename: str = "TOKEN.txt", depth: int = 2, *, strip: bool = True, default: T | ellipsis = ...) -> str | T:
		"""Get the nearest file with filename equal to given `filename` and return its stripped contents (unless specified not to strip with `strip=False`).
		Args:
			filename: The name of the file to search for.
			depth: How many parent directories to search through.
			strip: Whether to strip the contents of the file.
			default: If provided, this value will be returned if no file is found instead of raising an error.

		Returns:
			token: The contents of the found file, stripped if `strip=True`, or `default` if no file is found and `default` is provided.

		Raises:
			FileNotFoundError: If no file is found and `default` is not provided.

		"""

		original_path = p.Path.cwd().absolute()

		path = original_path / filename

		for i in range(depth + 1):
			path = (original_path / "/".join([".."] * i)) / filename
			if path.is_file():
				token_str = path.read_text()
				if not strip:
					token_str = token_str.strip()

				return token_str

		if default is not ...:
			return default

		msg = f"Unable to locate token file: {filename}"
		raise FileNotFoundError(msg)
