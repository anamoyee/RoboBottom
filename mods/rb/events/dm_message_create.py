from datetime import datetime

import hikari
from common import BOT
from mods._.config import S as S1
from mods._.db import UserDB
from mods.rb.models import Reminder
from prelude import *


@BOT.listen()
async def on_message_create(event: hikari.DMMessageCreateEvent):
	if not event.is_human:
		return

	with UserDB(event.author.id) as user:
		prof = user.ensure_profile(event.author)

		now = datetime.now(tz=S1.TZINFO)

		if event.content is None:
			raise RuntimeError("Missing event.content intent!")

		try:
			rem = await Reminder.from_str(
				event.content,
				now=now,
				user=event.author.id,
				chan_author=event.author,
				chan_guild=None,
				chan_here_channel=event.channel_id,
			)
		except Reminder.InvalidSyntaxError as e:
			await event.message.respond(e.display(), reply=event.message)
			return

		await (
			(rem)
			.schedule_to_profile(prof)
			.respond_with(
				event.message.respond,
				display=Reminder.ScheduledDisplay(user=user, prof=prof),
				ephemeral=False,
			)
		)
