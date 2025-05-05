from types import ModuleType

from prelude import *


class Mod(RbBM):
	"""Expansion pack to the bot's functionality, for example `_` (built-ins), or a user-made mod."""

	name: str
	"""Name of this mod."""
	pymodule: ModuleType
	"""The python module of this mod."""
