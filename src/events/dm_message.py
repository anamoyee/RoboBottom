import hikari

from .. import templates
from ..bot import BOT


@BOT.listen()
async def on_dm_message_create(event: hikari.DMMessageCreateEvent):
	if not event.is_human:
		return

	await event.message.respond(
		**templates.message.reminder_scheduling.successful(">>nya<<"),
		reply=event.message,
	)
