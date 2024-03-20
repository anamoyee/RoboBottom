from r00_imports import *

if True:  # Typed Dicks

  class ActivityTD(TD):
    name: str
    type: NotRequired[Unpack[hikari.ActivityType]]
    state: NotRequired[str | None]
    url: NotRequired[str | None]


if True:  # Reminder:

  class CTF:
    NONE = 0
    HASH_HIDDEN = 1 << 0
    IMPORTANT = 1 << 1
    NO_PRIORITY = 1 << 2

  CTFLookup: dict[str, int] = {
    '#': CTF.HASH_HIDDEN,
    '!': CTF.IMPORTANT,
    '=': CTF.NO_PRIORITY,
  }

  @dataclass(init=False)
  class Reminder:
    uuid: int = tcr.Null
    """Unique ID for each reminder."""
    user: int = tcr.Null
    """The Discord Snowflake of the user who requrested the reminder."""
    unix: int = tcr.Null
    """The unix timestamp of when the reminder should be triggered."""
    created_at: int = tcr.Null
    """The unix timestamp of when the reminder was created."""
    text: str = tcr.Null
    """The text body of the reminder."""
    tstr: str = tcr.Null
    """The original timestr (before to_int) used to schedule the reminder."""
    flags: int = tcr.Null
    """The reminder's True/False settings (hidden, important)."""

    def __init__(
      self,
      user: int,
      unix: int,
      created_at: int,
      text: str,
      tstr: str,
      flags: int,
    ) -> None:
      if not tcr.discord.is_snowflake(user):
        raise ValueError('user must be a valid snowflake')

      self.uuid = get_uwuid().int
      self.user = int(user)
      self.unix = int(unix)
      self.created_at = int(created_at)
      self.text = text
      self.tstr = tstr
      self.flags = flags

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
