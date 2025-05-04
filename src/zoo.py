from common import BOT, zoo
from common.events import ModsLoadedEvent
from prelude import *
from tcrutils.extract_error import print_exception_with_traceback

from .mod_loader import ZooModDependencyError, load_mods_from_directory


@BOT.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
	if "_" in sys.modules:  # Prevent duplicate fire
		return

	try:
		try:
			zoo.mods = await load_mods_from_directory(p.Path(__file__).parent.parent / "mods")
		except ZooModDependencyError as e:
			c.critical(f"mods: {e}")
			exit(1)

		await ModsLoadedEvent().emit_excgroup()
	except Exception as e:
		print_exception_with_traceback(e)
		exit(1)  # Do not let the exception propagate, instead shut the bot down at this stage.
