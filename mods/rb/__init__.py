from prelude import *

logger = get_logger(__name__)


async def load() -> None:
	from common.events import ModsLoadedEvent

	...

	from . import lang

	...  # Load translations first

	from . import commands, db, loops, models
	from . import config as _config

	@ModsLoadedEvent.subscribe
	async def on_mods_loaded(event: ModsLoadedEvent):
		loops.send_reminder_loop.start()
