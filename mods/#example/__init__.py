from _.db import UserDB


async def load() -> None:
	"""Construct and setattr your mod exports, if any."""


async def loaded_print() -> str | object | None:
	"""Return a str to get it printed to the screen as a log that your mod successfully loaded.

	If None is returned, nothing will be printed (You will be able to print something yourself).
	If this function is not defined, a default loaded message will be printed
	If a non-str object is returned it will be rich-printed if possible.
	"""

	return f"mods.{__name__}: Loaded successfully but with a custom message!"
