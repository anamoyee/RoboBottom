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
) -> None:
	with UserDB(ctx.author.id) as user:
		prof = user.ensure_profile(ctx)

		await (
			Reminder(
				text=text,
				unix=datetime.now(tz=S1.TZINFO) + Δ(seconds=3),
			)
			.schedule_to_profile(prof)
			.respond_to(
				display=Reminder.ScheduledDisplay(dbkey=ctx.author.id, user=user, prof=prof),
				ctx=ctx,
				ephemeral=ephemeral,
			)
		)
