import r02_settings as S
import r05_embed as m_embed
import r06_db as m_db
import r07_syncs as m_syncs
import r08_asyncs as m_asyncs
from r00_imports import *

if True:  # Errors
  class TextErrpondError(Exception):
    """Represents an error that should be handled by text_errponding. Provides a shorthand for it: e.execute(ctx)."""

    async def execute(self, ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent, **text_errpond_kwargs):
      await m_asyncs.text_errpond(ctx, self.title, self.description, **text_errpond_kwargs)

    def __init__(self, title: str, description: str) -> None:
      self.title = title
      self.description = description
      super().__init__()

if True:  # Typed Dicks

  class ActivityTD(TD):
    name: str
    type: NotRequired[Unpack[hikari.ActivityType]]
    state: NotRequired[str | None]
    url: NotRequired[str | None]

  class CreatedByTD(TD):
    id: int
    name: str

if True:  # Reminder:

  class CTF:
    NONE = 0
    """No special flags are set."""
    HASH_HIDDEN = 1 << 0
    """The reminder contents are hidden from the user until the reminder is triggered."""
    IMPORTANT = 1 << 1
    """Upon invokation the reminder is delivered with a user @mention."""

  CTF_DICT: dict[str, int] = {
    '#': CTF.HASH_HIDDEN,
    '!': CTF.IMPORTANT,
  }

  @atr.s(kw_only=True)
  class Reminder:
    """Represends a reminder contaning various information about itself and its owner."""

    user: int = atr.field(validator=lambda _obj, _attr, value: tcr.discord.is_snowflake(value), converter=int, hash=False, eq=False)
    """The Discord Snowflake of the user who requested the reminder."""
    unix: int = atr.field(converter=int, hash=False, eq=False)
    """The unix timestamp of when the reminder was created."""
    text: str = atr.field(validator=atr.validators.instance_of(str), hash=False, eq=False)
    """The text body of the reminder."""
    tstr: str = atr.field(validator=atr.validators.instance_of(str), hash=False, eq=False)
    """The original timestr (before to_int) used to schedule the reminder."""
    offset: int = atr.field(validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The seconds the tstr evaluated to at the time of scheduling."""
    flags: CTF = atr.field(validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The unix timestamp of when the reminder should be triggered."""
    ctx_message_id: hikari.Snowflake | None = atr.field(default=None, hash=False, eq=False)
    """The message ID of the reminder schedule message."""
    created_at: int = atr.field(factory=lambda: int(time.time()), validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The reminder's True/False settings (hidden, important)."""
    timeout: int = atr.field(default=0, validator=atr.validators.instance_of(int), hash=False, eq=False)
    """Added to unix when the reminder cannot be delivered (user blocked or unavailable) bot will periodically try to re-deliver the reminder."""
    uuid: int = atr.field(factory=lambda: get_uwuid().int, validator=atr.validators.instance_of(int | tcr.types.HexInt), converter=tcr.types.HexInt, eq=True, hash=True)
    """Unique ID for each reminder."""
    priority: int = atr.field(default=0, validator=atr.validators.instance_of(int), hash=False, eq=False)
    """Priority of the reminder. Higher priority reminders will be marked with `>` symbols and their P# level in reminder list (`.`)."""
    recursion_tstr: str = atr.field(default='', validator=atr.validators.instance_of(str), hash=False, eq=False)
    """If == '' the recursion is disabled. Else: when this reminder is triggered, reschedule it with a given interval."""
    attachments: t.Sequence[hikari.Attachment] = atr.field(default=(), hash=False, eq=False)
    """The attachments stored in the reminder."""

    async def send(self, bot: hikari.GatewayBot) -> None:
      """Send the reminder to the user."""

      channel = await bot.rest.create_dm_channel(self.user)
      await channel.send(m_embed.EMBED.reminder(self), attachments=self.attachments)

    def expired(self) -> bool:
      """Return True if the reminder should be delivered."""
      return self.unix < time.time()

    def expired_for(self) -> int:
      """Return the number of seconds this reminder was in the expired() == True state.

      Can be negated to get the time remaining.
      """
      return int(time.time() - self.unix)

    def remove_from_db(self) -> None:
      """Remove the reminder from the user's database.

      Raises value error if the reminder is not in the database.
      """
      db: m_db.U = m_db.Database(self.user)
      r = db['r']
      r = [x for x in r if x.uuid != self.uuid]
      db['r'] = r

    def flags_as_discord_text(self) -> str:
      """### Return `''` or something like '\\`!#\\` '."""
      if not self.flags:
        return ''
      return f'`{"".join(k for k, v in CTF_DICT.items() if v & self.flags)}` '

    def is_flag(self, flags: CTF) -> bool:
      """Return True if all the passed flags are set else False."""
      return bool(self.flags & flags)

    def fetch_index(self) -> int:
      """Return the index that this reminder lies at in that user's `db['r']`, May raise ValueError if the reminder is not present (was deleted at some point or never appended)."""
      db: m_db.U = m_db.Database(self.user)
      r = db['r']
      return r.index(self)

    def __str__(self) -> str:
      if self.flags & CTF.HASH_HIDDEN:
        return m_syncs.somehow_you_managed_to('display a hidden reminder', about_to=True)

      return tcr.cut_at(f'{self.flags_as_discord_text()}**{self.text.replace("**", "^^")}** ({tcr.discord.IFYs.timeify(self.unix, style="R")})', n=S.S.REMINDER_LIST_MAX_CHARS_PER_REMINDER)

    def __repr__(self) -> str:
      return f'<|flags={self.flags_as_discord_text().replace("`", "").strip()}, text={tcr.cut_at(self.text, 32)}, unix={self.unix}, user={self.user}, tstr={self.tstr}|>'

    def __tcr_display__(self=None, **kwargs):
      if kwargs.get('syntax_highlighting', False):
        return tcr.fmt_iterable(
          tcr.clean_dunder_dict((self if self is not None else Reminder).__dict__),
          _force_next_type=Reminder,
          _i_am_class=bool(self is None),
          **kwargs,
        )
      else:
        return tcr.fmt_iterable(
          tcr.clean_dunder_dict((self if self is not None else Reminder).__dict__),
          **kwargs,
        )


if True:  # User Settings

  @atr.s
  class UserSettings:
    timezone: str = atr.ib('pl-PL')
