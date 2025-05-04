from prelude import *


async def load() -> None:
	from common.events import ModsLoadedEvent

	...

	from . import lang

	...  # Load translations first

	from . import commands, db, models
	from . import config as _config

	@ModsLoadedEvent.subscribe
	async def on_mods_loaded(event: ModsLoadedEvent):
		c(event)
