from prelude import *

logger = get_logger(__name__)


async def load() -> None:
	from common.events import ModsLoadedEvent

	...

	from . import lang

	...  # Load translations first

	from . import commands, db, models
	from . import config as _config
