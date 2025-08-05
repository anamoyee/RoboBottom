import re
from collections.abc import Awaitable, Callable, Iterable
from datetime import datetime
from datetime import timedelta as Δ
from enum import IntFlag
from functools import reduce
from typing import TYPE_CHECKING, Literal, Self

import lark
import str2td
from common import BOT
from hikari import Embed
from mods._.config import S
from mods._.db.model_user import User
from mods._.errors import ModError
from mods._.tools import ephemeral_from_bool
from mods.rb.tools import try_fetch_channel_from_str
from tcrutils.codeblock import codeblock

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
			cls.HIDDEN: "?",
		}


class ReminderErrorFlag(IntFlag):
	NONE = 0
	INVALID_CHANNEL = 1 << 0


class Reminder(Object):
	user: int
	"""The discord ID of the owner of this reminder."""
	text: str
	"""The text content of this reminder."""
	unix: datetime
	"""The time at which this reminder is due."""
	flag: ReminderFlag = 0
	"""The feature flags associated with this reminder."""
	err_flag: ReminderErrorFlag = 0
	"""The error flags associated with this reminder."""
	chan: int | None = None
	"""The ID of the target channel for this reminder. If None, the primary channel"""

	@pd.field_validator("unix", mode="before")
	@classmethod
	def ensure_tzaware_unix(cls, value: datetime) -> datetime:
		if value.tzinfo is None:
			raise ValueError(f"{cls.__name__}.unix must be timezone-aware")

		return value

	@classmethod
	async def from_str(
		cls,
		s: str,
		/,
		now: datetime,
		*,
		user: int,
		chan_author: hikari.User,
		chan_guild: hikari.GatewayGuild | None,
		chan_here_channel: hikari.TextableChannel,
	) -> Self:
		dct: dict[str, str] = {}

		s = s.strip()

		PAT = re.compile(r"^([^\s=])=(\S*)")
		while match := re.match(PAT, s):
			s = s[match.end() :]

			k, v = match.groups()

			k = {
				"#": "channel",  # #=123 -> channel=123
				"&": "repeat",
				"!": "important",
				"?": "hidden",
			}.get(k, k)

			dct[k] = v

		s = s.strip()

		dct = {k.lower(): v for k, v in dct.items()}

		if " " not in s:
			s = f"{s} {s}"

		unix_str, s = s.split(" ", 1)

		flag, s = ReminderFlag.from_str_prefix(s)

		chan_str = dct.pop("channel", None)

		if dct.pop("important", None) is not None:
			flag |= ReminderFlag.IMPORTANT

		if dct.pop("hidden", None) is not None:
			flag |= ReminderFlag.HIDDEN

		try:
			δ = str2td.str2td(unix_str, now=now)
		except lark.LarkError as e:
			raise cls.InvalidSyntaxError(e) from e

		return cls(
			user=user,
			text=s,
			unix=now + δ,
			flag=flag,
			chan=(
				None  # TODO: change to default to: "here if here in registered_channels else primary_channel"
				if chan_str is None
				else (
					await try_fetch_channel_from_str(
						chan_str,
						author=chan_author,
						guild=chan_guild,
						here_channel=chan_here_channel,
					)
				)
			),
		)

	def sort_key(self):
		return self.unix

	def is_due(self, correction_factor: Δ = Δ(seconds=-1)) -> bool:
		"""Return True if this reminder is past its due date. If correction factor is negative, return True that much earlier, if it's positive return that much later."""
		return (self.unix + correction_factor) <= datetime.now(S.TZINFO)

	def to_discord_timestamp(self, style: Literal["t", "T", "d", "D", "f", "F", "R"] = "f") -> str:
		return f"<t:{int(self.unix.timestamp())}:{style}>"

	async def send(self, display: "Reminder.RemindDisplay"):
		"""Send this reminder as a message in a DM to the user (or any channel they specified). This is used when the reminder is due."""
		display._set_reminder(self)

		channel = await self.fetch_channel()

		return await channel.send(**display.to_hikari_dict())

	async def respond_with[T](
		self,
		respond: Callable[..., Awaitable[T]],
		*,
		display: "Reminder._DisplayBase",
		ephemeral: bool = False,
	) -> T:
		"""Respond with this reminder to an arc.GatewayContext."""
		display._set_reminder(self)

		dct = display.to_hikari_dict()

		dct["flags"] |= ephemeral_from_bool(ephemeral)

		return await respond(**dct)

	def schedule_to_profile(self, profile: "RbProfile"):
		"""Save this reminder in the database for later sending.

		## This requires further writeback, this call needs to be in a with UserDB() statement.
		"""

		profile.reminders.append(self)
		profile.sort_reminders()

		return self

	async def fetch_channel(self) -> hikari.TextableChannel | hikari.DMChannel:
		if self.chan is not None:
			try:
				channel = await BOT.rest.fetch_channel(self.chan)

				if not isinstance(channel, hikari.TextableChannel):
					raise RuntimeError(f"Reminder.fetch_channel: {self.chan=} is not a TextableChannel.")  # noqa: TRY004 <-- Not a type issue, the self.chan value is invalid.
			except (hikari.NotFoundError, RuntimeError):
				self.err_flag |= ReminderErrorFlag.INVALID_CHANNEL
				# fall through to primary channel fallback
			else:
				return channel

		return await (await BOT.rest.fetch_user(self.user)).fetch_dm_channel()

	if True:  # Reminder Errors

		class InvalidSyntaxError(ModError):
			"""Raised when the user provided invalid reminder due time syntax."""

			def __init__(
				self,
				lark_error: lark.LarkError,
				/,
			) -> None:
				self.lark_error = lark_error

			def display(self):
				return f"There an issue interpreting the reminder due time: {codeblock(str(self.lark_error), max_length=1800)}"

	if True:  # class Display

		class _DisplayBase:
			rem: "Reminder"

			def __init__(self, *, user: User, prof: "RbProfile") -> None:
				self.user = user
				self.prof = prof

			def _set_reminder(self, reminder: "Reminder", /) -> None:
				self.rem = reminder

			def to_embed_description(self) -> str:
				text = self.rem.text

				if self.rem.flag & ReminderFlag.HIDDEN:
					text = f"||{simple_escape_text(text, escapes=('||',))}||"

				return text

			def to_message_flags(self) -> hikari.MessageFlag:
				return hikari.MessageFlag.NONE

			def to_content(self) -> hikari.UndefinedOr[str]:
				return hikari.UNDEFINED

			def to_embeds(self) -> list[Embed]:
				return []

			def to_hikari_dict(self) -> dict:
				return {
					"content": self.to_content(),
					"user_mentions": True,
					"embeds": self.to_embeds(),
					"flags": self.to_message_flags(),
				}

		class RemindDisplay(_DisplayBase):
			def to_content(self) -> hikari.UndefinedOr[str]:
				if not self.rem.flag & ReminderFlag.IMPORTANT:
					return hikari.UNDEFINED

				return f"# <@{self.rem.user}>"

			def to_embeds(self) -> list[Embed]:
				return [
					Embed(
						title="🔔 Reminder!",
						description=self.to_embed_description(),
						color=0xFFFF00,
					)
				]

		class ScheduledDisplay(_DisplayBase):
			def to_content(self) -> str:
				return f"Okay! Will remind you {self.rem.to_discord_timestamp(style='R')}"
