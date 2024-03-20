from r07_asyncs import *


class RBSettingsError(Exception):
  def __init__(
    self,
    *args: str | object,
    syntax_highlighting=True,
    force_no_indent=True,
    **kwargs,
  ) -> None:
    args = [
      (
        x
        if isinstance(x, str)
        else tcr.fmt_iterable(
          x,
          syntax_highlighting=syntax_highlighting and (not TESTMODE),
          force_no_indent=force_no_indent,
          **kwargs,
        )
      )
      for x in args
    ]
    s = fg('red') + attr('bold') + '%s' + attr(0)
    s = ''.join(args) if TESTMODE else (s % ''.join(args))

    super().__init__(s)


# Don't skip validation, it also modifies some values which is vital to the program.
if True:  # FORCE_TESTMODE
  if S.FORCE_TESTMODE not in (_it := (None, True, False)):
    raise RBSettingsError('S.FORCE_TESTMODE must be either of: ', _it)
  S.FORCE_TESTMODE = bool(S.FORCE_TESTMODE)

if True:  # STATUS
  if S.STATUS not in (
    _it := (
      hikari.Status.ONLINE,
      hikari.Status.IDLE,
      hikari.Status.DO_NOT_DISTURB,
      hikari.Status.OFFLINE,
    )
  ):
    raise RBSettingsError('S.STATUS must be either of: ', _it, force_no_indent=0, let_no_indent=0)

if True:  # ACTIVITY
  if not (S.ACTIVITY is None or isinstance(S.ACTIVITY, dict)):
    raise RBSettingsError('S.ACTIVITY must be either None or dict')
  if not tcr.able(hikari.Activity, **S.ACTIVITY):
    raise RBSettingsError(
      'Invalid S.ACTIVITY configuration. ' "Check hikari.Activity's arguments for proper config, got: \n",
      S.ACTIVITY,
      force_no_indent=False,
    )
  S.ACTIVITY['name'] += testmode()
  S.ACTIVITY = hikari.Activity(**S.ACTIVITY)

if True:  # BANNER & BANNER_COLORS
  if not (S.BANNER is None or isinstance(S.BANNER, str)):
    raise RBSettingsError('S.BANNER must be None or str, got: ', type(S.BANNER))

  if (
    (not isinstance(S.BANNER_COLORS, tuple | list))
    or (len(S.BANNER_COLORS) != 3)
    or (not isinstance(S.BANNER_COLORS[0], int))
    or (not isinstance(S.BANNER_COLORS[1], str))
    or (not isinstance(S.BANNER_COLORS[2], str))
  ):
    raise RBSettingsError(
      'S.BANNER_COLORS must be a tuple[int, str, str],\n' 'The first value is the cutoff point, the second value is the color before cutoff and the third is the color after cutoff. Got: ',
      S.BANNER_COLORS,
      let_no_indent=False,
      force_no_indent=False,
    )

if True:  # DEFAULT_ENABLED_GUILDS
  if isinstance(S.DEFAULT_EANBLED_GUILDS, int):
    S.DEFAULT_EANBLED_GUILDS = (S.DEFAULT_EANBLED_GUILDS,)
  if not (S.DEFAULT_EANBLED_GUILDS is None or isinstance(S.DEFAULT_EANBLED_GUILDS, tuple | list)):
    raise RBSettingsError(
      'S.DEFAULT_EANBLED_GUILDS must be either None or tuple[int] (or empty tuple), got: ',
      repr(S.DEFAULT_EANBLED_GUILDS),
    )
  if S.DEFAULT_EANBLED_GUILDS is None:
    S.DEFAULT_EANBLED_GUILDS = ()
  if not all(tcr.discord.is_snowflake(x, allow_string=False) for x in S.DEFAULT_EANBLED_GUILDS):
    raise RBSettingsError(
      'S.DEFAULT_ENABLED_GUILDS must be a tuple of Snowflakes, ints that are in range((1 << 64) - 1), got: ',
      repr(S.DEFAULT_EANBLED_GUILDS),
    )

  if isinstance(S.DEV_EANBLED_GUILDS, int):
    S.DEV_EANBLED_GUILDS = (S.DEV_EANBLED_GUILDS,)
  if not (S.DEV_EANBLED_GUILDS is None or isinstance(S.DEV_EANBLED_GUILDS, tuple | list)):
    raise RBSettingsError(
      'S.DEV_EANBLED_GUILDS must be either None or tuple[int] (or empty tuple), got: ',
      repr(S.DEV_EANBLED_GUILDS),
    )
  if S.DEV_EANBLED_GUILDS is None:
    S.DEV_EANBLED_GUILDS = ()
  if not all(tcr.discord.is_snowflake(x, allow_string=False) for x in S.DEV_EANBLED_GUILDS):
    raise RBSettingsError(
      'S.DEFAULT_ENABLED_GUILDS must be a tuple of Snowflakes, ints that are in range((1 << 64) - 1), got: ',
      repr(S.DEV_EANBLED_GUILDS),
    )

if True:  # Embed Colors
  if not isinstance(S.EMBED_COLORS, dict):
    raise RBSettingsError('S.EMBED_COLORS must be a dict. got: ', type(S.EMBED_COLORS))
  if not all(isinstance(x, str) for x in S.EMBED_COLORS):
    raise RBSettingsError('All keys of S.EMBED_COLORS must be str')
  if not all((isinstance(x, int) or (isinstance(x, str) and tcr.able(int, c(x, type(x)).replace('#', '0x'), base=0))) for x in S.EMBED_COLORS.values()):
    raise RBSettingsError('All values of S.EMBED_COLORS must be in supported formats')
  S.EMBED_COLORS = {k: v if isinstance(v, int) else int(v.replace('#', '0x'), base=0) for k, v in S.EMBED_COLORS.items()}
  if not all((x in range(0xFFFFFF + 1)) for x in S.EMBED_COLORS.values()):
    raise RBSettingsError('All values of S.EMBED_COLORS must be valid hex colors must be in range(0xffffff + 1)')
