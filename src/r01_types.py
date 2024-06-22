import hikari.errors
import r02_settings as S
import r04_bot as m_bot
import r05_embed as m_embed
import r06_db as m_db
import r07_syncs as m_syncs
import r08_asyncs as m_asyncs
from r00_imports import *

if True:  # User Settings

  @atr.s(kw_only=True)
  class UserSettings:
    timezone: str = atr.ib(default='pl-PL')
    setting1: str = atr.ib(default='value1')
    setting2: str = atr.ib(default='value2')

    def export(self) -> dict:
      return {x.name: getattr(self, x.name) for x in self.__attrs_attrs__}


if True:  # Errors

  class TextErrpondError(Exception):
    """Represents an error that should be handled by text_errponding. Provides a shorthand for it: e.execute(ctx)."""

    async def execute(self, ctx_or_event: arc.GatewayContext | hikari.GuildMessageCreateEvent, **text_errpond_kwargs):
      await m_asyncs.text_errpond(ctx_or_event, self.title, self.description, **text_errpond_kwargs)

    def __init__(self, title: str, description: str) -> None:
      self.title = title
      self.description = description
      super().__init__()

  class ReminderFromExportMismatchedKeysError(Exception):
    extra: set[str]
    missing: set[str]

    def __init__(self, *, extra: set[str], missing: set[str]) -> None:
      self.extra = extra
      self.missing = missing
      super().__init__()

if True:  # Database stuff

  class U(TD):
    r: list['Reminder'] = list
    settings: 'UserSettings' = UserSettings
    first_seen: int = lambda: int(time.time())
    last_taken_backup: int = int

  class V(TD):
    revolution: int = int

  class G(TD):
    banned: set[int] = set


if True:  # Typed Dicks

  class ActivityTD(TD):
    name: str
    type: NotRequired[Unpack[hikari.ActivityType]]
    state: NotRequired[str | None]
    url: NotRequired[str | None]

  class CreatedByTD(TD):
    id: int
    name: str

  if True:  # Export

    class ExportedDataReminderTD(TD):
      unix: int
      text: str
      tstr: str
      offset: int
      flags: int
      created_at: int
      priority: int
      recursion_tstr: str
      attachment_urls: list[str]

    class ExportedDataTD(TD):
      settings: UserSettings
      reminders: list[ExportedDataReminderTD]


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
    """The unix timestamp of when the reminder should be triggered."""
    text: str = atr.field(validator=atr.validators.instance_of(str), hash=False, eq=False)
    """The text body of the reminder."""
    tstr: str = atr.field(validator=atr.validators.instance_of(str), hash=False, eq=False)
    """The original timestr (before to_int) used to schedule the reminder."""
    offset: int = atr.field(validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The seconds the tstr evaluated to at the time of scheduling."""
    flags: CTF = atr.field(validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The reminder's flag settings (hidden, important)."""
    ctx_message_id: hikari.Snowflake | None = atr.field(default=None, hash=False, eq=False)
    """The message ID of the reminder schedule message."""
    created_at: int = atr.field(factory=lambda: int(time.time()), validator=atr.validators.instance_of(int), hash=False, eq=False)
    """The unix timestamp of when the reminder was created."""
    timeout: int = atr.field(default=0, validator=atr.validators.instance_of(int), hash=False, eq=False)
    """Added to unix when the reminder cannot be delivered (user blocked or unavailable) bot will periodically try to re-deliver the reminder."""
    uuid: int = atr.field(factory=lambda: get_uwuid().int, validator=atr.validators.instance_of(int | tcr.types.HexInt), converter=tcr.types.HexInt, eq=True, hash=True)
    """Unique ID for each reminder."""
    priority: int = atr.field(default=0, validator=atr.validators.instance_of(int), hash=False, eq=False)
    """Priority of the reminder. Higher priority reminders will be marked with `>` symbols and their P# level in reminder list (`.`)."""
    recursion_tstr: str = atr.field(default='', validator=atr.validators.instance_of(str), hash=False, eq=False)
    """If == '' the recursion is disabled. Else: when this reminder is triggered, reschedule it with a given interval."""
    attachments: t.Sequence[hikari.Attachment | hikari.URL] = atr.field(default=(), hash=False, eq=False)
    """The attachments stored in the reminder."""

    async def send(self, auto_safemode: bool = True) -> None:
      """Send the reminder to the user."""

      if auto_safemode:
        try:
          channel = await m_bot.BOT.rest.create_dm_channel(self.user)
          await channel.send(**m_embed.RESP.reminder(self))
        except hikari.HikariError:
          await self.send_safemode()
      else:
        channel = await m_bot.BOT.rest.create_dm_channel(self.user)
        await channel.send(**m_embed.RESP.reminder(self))

    async def send_safemode(self) -> None:
      """If `.send()` fails use this, prefferably use `.send(auto_safemode=True)` wchich does this automatically on fail."""

    def export(self) -> ExportedDataReminderTD | None:
      """Export the reminder to dict. Forget the user, only retain reminder structure."""
      if self.is_flag(CTF.HASH_HIDDEN):
        return None

      return {
        'unix': self.unix,
        'text': self.text,
        'tstr': self.tstr,
        'offset': self.offset,
        'flags': self.flags,
        'created_at': self.created_at,
        'priority': self.priority,
        'recursion_tstr': self.recursion_tstr,
        'attachment_urls': [x.url for x in self.attachments],
      }

    @staticmethod
    def from_export(rem: ExportedDataReminderTD, user: int) -> 'Reminder':
      rem_keys: set[str] = set(rem.keys())
      allowed_keys: set[str] = set(ExportedDataReminderTD.__annotations__.keys())

      if rem_keys != allowed_keys:
        extra_keys = rem_keys - allowed_keys
        missing_keys = allowed_keys - rem_keys

        raise ReminderFromExportMismatchedKeysError(extra=extra_keys, missing=missing_keys)

      return Reminder(
        user=user,
        unix=rem['unix'],
        text=rem['text'],
        tstr=rem['tstr'],
        offset=rem['offset'],
        flags=rem['flags'],
        created_at=rem['created_at'],
        priority=rem['priority'],
        recursion_tstr=rem['recursion_tstr'],
        attachments=[hikari.URL(x) for x in rem['attachment_urls']],
      )

    def expired(self) -> bool:
      """Return True if the reminder should be delivered."""
      return self.unix < time.time()

    def expired_for(self) -> int:
      """Return the number of seconds this reminder was in the expired() == True state.

      Can be negated to get the time remaining.
      """
      return int(time.time() - self.unix)

    def remove_from_db(self, db: 'm_db.Database | None' = None) -> None:
      """Remove the reminder from the user's database.

      Raises value error if the reminder is not in the database.
      """
      if db is None:
        db: m_db.U = m_db.Database(self.user)
      else:
        if not isinstance(db, m_db.Database) or db.alnum_id != str(self.user):
          raise ValueError(f'Incompatible database.')
      r = db['r']
      r = [x for x in r if x.uuid != self.uuid]
      db['r'] = r

    def flags_as_listabbrev(self) -> str:
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

    def attachments_as_listabbrev(self) -> str:
      """Simillar to `flags_as_listabbrev` but for attachments."""

      FILE_EMOJIS = [
        #  '📝',
        #  '🖼',
        '📂',
      ]

      with tcr.random_seed_lock(self.uuid) as rng:
        if not self.attachments:
          return ''
        if len(self.attachments) <= 3:
          return f'{len(self.attachments)*rng.choice(FILE_EMOJIS)} '
        return f'{len(self.attachments)}{rng.choice(FILE_EMOJIS)} '

    def display_text(self) -> str:
      if self.is_flag(CTF.HASH_HIDDEN):
        return f'`{"".join(ch for ch in rng.choices(string.ascii_letters + string.digits, k=tcr.clamp(3, len(self.text)+rng.randint(-3, 3), 50)))}`'
      return self.text

    def display_text_list_item(self) -> str:
      displayed_text = self.display_text()

      if not self.is_flag(CTF.HASH_HIDDEN):
        displayed_text = tcr.discord.remove_markdown(displayed_text)

      return displayed_text.replace('\n', '')

    def __str__(self) -> str:
      """The version displayed when viewing THE LIST of reminders. For the reminder itself and viewing it, it's managed manually."""
      # fmt: off
      text_front = f'{self.flags_as_listabbrev()}{self.attachments_as_listabbrev()}**'
      text_back  =                                                                  f'** ({tcr.discord.IFYs.timeify(self.unix, style="R")})'
      # fmt: on

      text = tcr.cut_at(
        self.display_text_list_item(),
        n=max(0, S.S.REMINDER_LIST_MAX_CHARS_PER_REMINDER - (len(text_front) + len(text_back))),
        shrink_links_visually_if_fits=True,
      )

      return text_front + text + text_back

    def __repr__(self) -> str:
      return f'/flags={self.flags_as_listabbrev().replace("`", "").strip()}, unix={self.unix}, user={self.user}, tstr={self.tstr}, text={tcr.cut_at(self.text, 32)}/'

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


if True:  # Helper structs

  class FallbackDict(dict):
    """In case of a missing key, execute a callable to get the default/fallback value."""

    fallback: Callable[[Self, Any], Any]

    def __init__(self, *args, fallback: Callable[[Self, Any], Any], write_missing_keys: bool = False, **kwargs):
      super().__init__(*args, **kwargs)
      self.fallback = fallback
      self.write_missing_keys = write_missing_keys

    def __missing__(self, k: Any):
      v = self.fallback(self, k)

      if self.write_missing_keys:
        self[k] = v

      return v
