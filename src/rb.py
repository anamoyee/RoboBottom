from tcrutils.extract_error import print_exception_with_traceback

from common import BOT
from common.events import ModsLoadedEvent
from mod_loader import MODS, ModDependencyError, load_mods_from_directory
from prelude import *


@BOT.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
	if "_" in sys.modules:  # Prevent duplicate fire
		return

	try:
		try:
			MODS.update(await load_mods_from_directory(p.Path(__file__).parent.parent / "mods"))
		except ModDependencyError as e:
			c.critical(f"mods: {e}")
			exit(1)

		await ModsLoadedEvent().emit_excgroup()
	except Exception as e:
		print_exception_with_traceback(e)
		exit(1)  # Do not let the exception propagate, instead shut the bot down at this stage.
