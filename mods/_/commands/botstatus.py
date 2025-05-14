import datetime
import sys
import time

import psutil
from common import ACL, BOT
from prelude import *

from .._version import __version__
from ..config import S
from ..lang import LANG


def get_memory_usage() -> float:
	"""Return memory usage by this python application in MiB."""
	return psutil.Process().memory_info().rss / (1024**2)


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.botstatus"))
async def cmd_botstatus(ctx: arc.GatewayContext) -> None:
	me = BOT.get_me()

	guild_number = len(await BOT.rest.fetch_my_guilds())

	ping_start_time = time.time()

	embed = (
		hikari.Embed(
			description=f"""
**Originally Created by:** **[Colon](https://gdcolon.com)** {S.EMOJI.fluff}
**This is a fan made recreation.** **[Here's Original](https://gdcolon.com/robotop/)**
**Version:** v{__version__}
**Uptime:** {UPTIME}
**Servers:** {guild_number}
**Python version:** v{".".join(str(x) for x in sys.version_info[:3])} (**光** v{hikari.__version__})
**Memory usage:** {get_memory_usage():.2f} MB
**Gearbot Reminders:** suck
"""[1:-1],
			color=S.COLOR.PRIMARY,
			# timestamp=datetime.datetime.now(tz=S.TZINFO),
		)
		.set_author(
			name=me.display_name,
			icon=me.make_avatar_url() or me.default_avatar_url,
		)
		.set_footer(
			f"Roundtrip Ping: ... • Heartbeat Latency: {BOT.heartbeat_latency * 1000:.0f}ms",
		)
	)

	await ctx.respond(embed)

	ping_end_time = time.time()
	ping = (ping_end_time - ping_start_time) * 1000

	embed.set_footer(f"Roundtrip Ping: {ping:.0f}ms • Heartbeat Latency: {BOT.heartbeat_latency * 1000:.0f}ms")

	await ctx.edit_initial_response(embed=embed)
