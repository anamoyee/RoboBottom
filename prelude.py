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
"""Whether the bot is running in testmode, as specified by the token."""
__TOKEN = __TOKEN.removeprefix("TEST:")


def get_logger(name: str):
	"""Get rb.{name} logger, used with __name__, this is made to differentiate it from `hikari`, `arc`, etc. loggers."""
	if not isinstance(name, str):  # strict check, due to f'{name}' converting it to string anyway and who wants a "*.<Whatever object at 0xbadbed>" logger anyway
		raise TypeError(f"get_logger called, but name isn't a str, found {name!r} instead.")

	return _logging.getLogger(f"rb.{name}")


class RbBM(pd.BaseModel):
	model_config = pd.ConfigDict(
		arbitrary_types_allowed=True,
		extra="forbid",
		validate_default=True,
		validate_assignment=True,
	)
