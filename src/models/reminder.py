import datetime

import hikari
import pydantic as pd
import tcrutils as tcr

from .. import models

# Separators n stuff
SPACE = " "
COMMA = ","
BANG = "!"


class Reminder(models.BM):
	expires_at: datetime.datetime
	"""When this Reminder is set to expire."""

	scheduled_at: datetime.datetime
	"""When this Reminder was scheduled."""

	text: str
	"""Text content of this Reminder."""

	channel_id: hikari.Snowflake
	"""The ID of the channel that this Reminder was scheduled in."""
	message_id: hikari.Snowflake
	"""The ID of the user message that scheduled this Reminder."""

	@classmethod
	def from_message_data(
		cls,
		*,
		content: str,
		channel_id: hikari.Snowflake,
		message_id: hikari.Snowflake,
		tz: datetime.timezone,
	) -> list["Reminder"]:
		scheduled_at = datetime.datetime.now(tz=tz)

		if " " not in content:
			content = f"{content} {content}"

		time_contents, text = content.split(" ", maxsplit=1)
		# , TODO: Modify text, like remove trailing typos

		time_parts = time_contents.split(",")

		built_reminders = []

		for time_part in time_parts:
			# , TODO: Currently mock time impl - forget about time_part
			tcr.void(time_part)
			expires_at = datetime.datetime.now(tz=tz) + datetime.timedelta(seconds=5)

			r = cls(
				expires_at=expires_at,
				scheduled_at=scheduled_at,
				text=text,
				message_id=message_id,
				channel_id=channel_id,
			)

			built_reminders.append(r)

		return built_reminders

	@classmethod
	def from_message_create_event(
		cls,
		*,
		event: hikari.MessageCreateEvent,
		tz: datetime.timezone,
	) -> list["Reminder"]:
		return cls.from_message_data(
			content=event.content,
			message_id=event.message_id,
			channel_id=event.channel_id,
			tz=tz,
		)
