from collections.abc import Iterable
from datetime import datetime
from datetime import timedelta as Δ
from functools import reduce
from typing import TYPE_CHECKING, Literal, Self

from common import BOT
from hikari import Embed
from mods._.config import S
from mods._.db import UserDB
from mods._.db.model_user import User
from mods._.tools import ephemeral_from_bool

from .. import db
from ._base import *

if TYPE_CHECKING:
	from ..db import RbProfile


def simple_escape_text(text, /, *, escapes: Iterable[str]) -> str:
	return reduce(lambda a, b: a.replace(b, "".join(f"\\{char}" for char in b)), escapes, initial=text)


class ReminderFlag(StrFlag):
	NONE = 0
	IMPORTANT = 1 << 0
	HIDDEN = 1 << 1

	@classmethod
	def make_symbol_associations(cls) -> dict[Self, str]:
		return {
			cls.IMPORTANT: "!",
			cls.HIDDEN: "#",
		}


class Reminder(Object):
	text: str
	unix: datetime
	flag: ReminderFlag = 0

	@pd.field_validator("unix", mode="before")
	@classmethod
	def ensure_tzaware_unix(cls, value: datetime) -> datetime:
		if value.tzinfo is None:
			raise ValueError(f"{cls.__name__}.unix must be timezone-aware")

		return value

	def sort_key(self):
		return self.unix

	def is_due(self, correction_factor: Δ = Δ(seconds=-1)) -> bool:
		"""Return True if this reminder is past its due date. If correction factor is negative, return True that much earlier, if it's positive return that much later."""
		return (self.unix + correction_factor) <= datetime.now(S.TZINFO)

	def to_discord_timestamp(self, style: Literal["t", "T", "d", "D", "f", "F", "R"] = "f") -> str:
		return f"<t:{int(self.unix.timestamp())}:{style}>"

	async def send(self, display: "Reminder._DisplayBase"):
		"""Send this reminder as a message in a DM to the user."""
		display._set_reminder(self)

		channel = await BOT.rest.create_dm_channel(display.dbkey)

		await channel.send(**display.to_hikari_dict())

	async def respond_to(self, *, display: "Reminder._DisplayBase", ctx: arc.GatewayContext, ephemeral: bool = False):
		"""Respond with this reminder to an arc.GatewayContext."""
		display._set_reminder(self)

		dct = display.to_hikari_dict()

		dct["flags"] |= ephemeral_from_bool(ephemeral)

		await ctx.respond(**dct)

	def schedule_to_profile(self, profile: "RbProfile"):
		"""Save this reminder in the database for later sending.

		## This requires further writeback, this call needs to be in a with UserDB() statement.
		"""

		profile.reminders.append(self)
		profile.sort_reminders()

		return self

	class _DisplayBase:
		rem: "Reminder"

		def __init__(self, *, dbkey: str | int, user: User, prof: "RbProfile") -> None:
			self.user = user
			self.prof = prof
			self.dbkey = str(dbkey)

		def _set_reminder(self, reminder: "Reminder", /) -> None:
			self.rem = reminder

		def to_embed_description(self) -> str:
			text = self.rem.text

			if self.rem.flag & ReminderFlag.HIDDEN:
				text = f"||{simple_escape_text(text, escapes='||')}||"

			return text

		def to_message_flags(self) -> hikari.MessageFlag:
			return hikari.MessageFlag.NONE

		def to_content(self) -> hikari.UndefinedOr[str]:
			return hikari.UNDEFINED

		def to_embed(self) -> hikari.UndefinedOr[Embed]:
			return hikari.UNDEFINED

		def to_hikari_dict(self) -> dict:
			return {
				"content": self.to_content(),
				"user_mentions": True,
				"embed": self.to_embed(),
				"flags": self.to_message_flags(),
			}

	class RemindDisplay(_DisplayBase):
		def to_content(self) -> hikari.UndefinedOr[str]:
			if not self.rem.flag & ReminderFlag.IMPORTANT:
				return hikari.UNDEFINED

			return f"# <@{self.dbkey}>"

		def to_embed(self) -> Embed:
			return Embed(
				title="🔔 Reminder!",
				description=self.to_embed_description(),
				color=0xFFFF00,
			)

	class ScheduledDisplay(_DisplayBase):
		def to_content(self) -> str:
			return f"Okay! Will remind you in: {self.rem.to_discord_timestamp(style='R')}"
