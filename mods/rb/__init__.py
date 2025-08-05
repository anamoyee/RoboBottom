import asyncio
from datetime import timedelta as Δ

from common import BOT
from prelude import *

logger = get_logger(__name__)


async def load() -> None:
	from common.events import ModsLoadedEvent

	...

	from . import lang

	...  # Load translations first

	from . import commands, db, events, models
	from . import config as _config
	from . import loops as m_loops

	if True:  # handle arc loops

		@ModsLoadedEvent.subscribe
		async def on_mods_loaded_start_loops(event: ModsLoadedEvent):
			def _has_loop_stopped(loop: arc.utils.loops._LoopBase):
				return not loop._task or loop._task.done()

			loops = [
				m_loops.send_reminder_loop,
			]

			for loop in loops:
				loop.start()

			@BOT.listen()
			async def _(event: hikari.StoppingEvent):
				MAX_STOP_TIMEOUT_δ = Δ(seconds=10)

				logger.info("Terminating arc loops...")

				for loop in loops:
					loop.stop()

				async def wait_until_stopped(loop):
					_ASYNCIO_SLEEP_δ = Δ(seconds=0.1)

					for _ in range(MAX_STOP_TIMEOUT_δ // _ASYNCIO_SLEEP_δ):  # 10sδ // .1sδ = 100iter
						if _has_loop_stopped(loop):
							return True
						await asyncio.sleep(_ASYNCIO_SLEEP_δ.total_seconds())
					return False  # Timed out

				results = await asyncio.gather(*[wait_until_stopped(loop) for loop in loops])

				for loop, stopped in zip(loops, results, strict=True):
					if not stopped:
						loop.cancel()
						logger.error(f"arc loop {loop._coro.__qualname__!r} did not .stop() in time (took >{MAX_STOP_TIMEOUT_δ.total_seconds()}s)")
