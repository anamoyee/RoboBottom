import logging as _logging
import os
import pathlib as p
import sys

import arc
import hikari
import miru
import pydantic as pd
from tcrutils.console import c
from tcrutils.string import get_token
from tcrutils.uptime import Uptime

if os.name != "nt":
	import asyncio

	import uvloop

	asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


UPTIME = Uptime()

ROOT_PATH = p.Path(__file__).parent
"""The path of the root directory of the bot files. For example the first `'/'` of `'/mods/_'`."""

os.chdir(ROOT_PATH)

__TOKEN = get_token()
"""The bot's token. Generally you will never use this variable, but it's here because i couldn't be bothered with making a file containing just this one line."""

TESTMODE = __TOKEN.startswith("TEST:")
"""Whether the bot is running in testmode (development mode), as specified by the token. Should be used sparingly, because it can cause unexpected bugs in prod, while not causing any in testmode."""
__TOKEN = __TOKEN.removeprefix("TEST:")


def get_logger(name: str):
	"""Get bot.{name} logger, used with __name__, this is made to differentiate it from `hikari`, `arc`, etc. loggers."""
	if not isinstance(name, str):
		# strict isinstance check (as opposed to just f-string {...}'ing it), due to f'{name}' converting it to string anyway and who wants a "*.<Whatever object at 0xbadbed>" logger anyway
		raise TypeError(f"get_logger called, but name isn't a str, found {name!r} ({type(name)!r}) instead.")

	return _logging.getLogger(f"bot.{name}")


class BM(pd.BaseModel):
	model_config = pd.ConfigDict(
		arbitrary_types_allowed=True,
		extra="forbid",
		validate_default=True,
		validate_assignment=True,
	)

	def __setstate__(self, state: dict[str]) -> None:
		state.setdefault("__pydantic_fields_set__", set())
		state.setdefault("__dict__", {})

		__pydantic_fields_set__: set[str] = {*state["__pydantic_fields_set__"]}

		for field_key, field_info in self.__pydantic_fields__.items():
			if field_key in __pydantic_fields_set__:
				continue

			if field_info.is_required():
				raise RuntimeError(
					f"{self.__class__.__name__}: Unable to reconstruct outdated object from the database since it does not contain the requied field: {field_key!r} (This field has no default constructor to recover/migrate the value with)"
				)

			state["__dict__"].setdefault(field_key, field_info.get_default(call_default_factory=True))
			state["__pydantic_fields_set__"].add(field_key)

		for field_key in __pydantic_fields_set__:
			if field_key not in self.__pydantic_fields__:
				get_logger(f"prelude.BM").warning(
					f"!!! DELETING UNKNOWN FIELD {field_key!r} ON {self.__class__.__name__}. If this was not intended (You did not just remove a field from a class declaration of a class inheriting from BM) THEN RESTORE DATABASE FROM BACKUP AND INVESTIAGE... (ah shit..!) This happened because the database schema does not have this field while the database entry did."
				)  # Scary!

				state["__dict__"].pop(field_key)
				state["__pydantic_fields_set__"].remove(field_key)

		return super().__setstate__(state)
