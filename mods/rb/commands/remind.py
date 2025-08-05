from datetime import datetime
from datetime import timedelta as Δ

from common import ACL, BOT
from mods._.config import S as S1
from mods._.db import UserDB
from mods._.tools import OPTION_EPHEMERAL
from prelude import *

from ..config import S
from ..lang import LANG
from ..models import Reminder


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.remind"))
async def cmd_remind(
	ctx: arc.GatewayContext,
	text: arc.Option[str, arc.StrParams(**LANG.get_arc_command("/.remind:text"))],
	ephemeral: OPTION_EPHEMERAL = False,
	here: arc.Option[bool, arc.BoolParams(**LANG.get_arc_command("/.remind:here"))] = False,
) -> None:
	with UserDB(ctx.author.id) as user:
		prof = user.ensure_profile(ctx.author)

		now = datetime.now(tz=S1.TZINFO)

		try:
			rem = await Reminder.from_str(
				text,
				now=now,
				user=ctx.author.id,
				chan_author=ctx.author,
				chan_guild=ctx.get_guild(),
				chan_here_channel=ctx.channel if here else None,
			)
		except Reminder.InvalidSyntaxError as e:
			await ctx.respond(e.display(), flags=hikari.MessageFlag.EPHEMERAL)

		await (
			(rem)
			.schedule_to_profile(prof)
			.respond_with(
				ctx.respond,
				display=Reminder.ScheduledDisplay(user=user, prof=prof),
				ephemeral=ephemeral,
			)
		)
