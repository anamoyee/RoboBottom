from types import ModuleType

from prelude import *
from tcrutils.decorator import instance


class Mod(ZooBM):
	"""Expansion pack to the zoo bot functionality, for example `_` (built-ins), or a user-made mod."""

	name: str
	"""Name of this mod."""
	pymodule: ModuleType
	"""The python module of this mod."""


@instance
class zoo(ZooBM):
	"""The read-only zoo state compiled at init, for example all items, all animals, all leaders, all installed modules.

	Modifying this at runtime may lead to undefined behavior.
	"""

	mods: dict[str, Mod] = pd.Field(default_factory=dict)
	"""dict[mod_name, Mod] of all mods loaded."""
