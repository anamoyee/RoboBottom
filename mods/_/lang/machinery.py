from collections.abc import Callable as _Callable
from pathlib import Path as _Path
from typing import Any as _Any

from hikari import Locale as L
from prelude import *
from tcrutils.import_ import load_package_dynamically as _load_package_dynamically
from tcrutils.lang import Lang as _Lang

from ..errors import ZooModError, _dataclass

if True:  # Errors

	class LangImportError(ZooModError):
		"""Base class for all errors related to lang imports."""

	@_dataclass
	class LangImportExecError(LangImportError):
		"""An error was raised when importing a lang module."""

		e: Exception

	class LangImportMissingOrMalformedOutputVariableError(LangImportError):
		"""The `_` variable is missing on the imported module."""


def from_directory[V = _Any](directory: _Path) -> dict[L | None, dict[str, V]]:
	"""## Load translations from a directory of .py files.

	- Find all .py files that are any of the stringified values of hikari.Locale enum variants + ".py" (where each filename's "_" is replaced with a hikari.Locale's "-")
	- Exec them & get the `_` variable
	- Return the `dict[Locale, dict[str, V]]`

	This also loads the `_.py` file with the Locale | None key set as None.
	"""

	MISSING = object()

	d = {None: MISSING}

	for file in directory.glob("*.py"):
		if not file.is_file():
			continue

		if "-" in file.stem:
			continue

		if file.stem == "_":
			l = None
		else:
			stem_replaced = file.stem.replace("_", "-")

			if stem_replaced not in L:
				continue

			l = L(stem_replaced)

		try:
			module = _load_package_dynamically(file)
		except Exception as e:
			raise LangImportExecError(e) from e

		if not hasattr(module, "_"):
			raise LangImportMissingOrMalformedOutputVariableError(f"`_` variable is missing from module {module.__name__!r}")

		if not isinstance(module._, dict):
			raise LangImportMissingOrMalformedOutputVariableError(f"`_` variable in module {module.__name__!r} is not a dict")

		if not all(isinstance(k, str) for k in module._):
			raise LangImportMissingOrMalformedOutputVariableError(f"`_` variable in module {module.__name__!r} contains non-string keys")

		d[l] = module._

	if d[None] is MISSING:
		d.pop(None)

	return d


def merge_directory[K1, K2, V](lang: _Lang[K1, K2, V], directory: _Path) -> int:
	_lang = from_directory(directory)

	for locale, pack in _lang.items():
		lang.merge_localepack(locale, pack)

	return len(_lang)


def merge_directory_and_log(lang: _Lang[L, str, str], directory: _Path, c_log: _Callable[[str], None], names: tuple[str, str] = ("language pack", "language packs")) -> None:
	c_log(f"loaded {(n := merge_directory(lang, directory))} {names[n != 1]}")


LANG = _Lang[L, str, str]()
"""All loaded language packs, when merging, it overrides any conflicting keys. (x[L][T] <- V => overriden)"""
POOLS = _Lang[L, str, tuple[str]](merge_func=lambda v1, v2: (*v1, *v2))
"""All loaded language pools (language packs where values are tuples of strings), when merging, it merges any conflicting keys, since they're tuples. (x[L][T] <- V => (*previous, *current) - This does not remove duplicates within the tuple though.)"""
