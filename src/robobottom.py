__import__('os').system('pip install --upgrade tcrutils') if 't' in __import__('sys').argv else ''  # fmt: skip

if True:  # \/ # Imports
  import os
  import sys
  from typing import NotRequired, TypedDict, Unpack

  import arc
  import hikari
  import miru
  import tcrutils as tcr
  from colored import attr, bg, fg
  from lightbulb.ext import tasks
  from tcrutils import console as c

if True:  # \/ # Types
  if True:  # \/ # Typed Dicks

    class ActivityTD(TypedDict):
      name: str
      type: NotRequired[Unpack[hikari.ActivityType]]
      state: NotRequired[str | None]
      url: NotRequired[str | None]

  if True:  # \/ # Errors

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

if True:  # \/ # Settings

  class S:
    """Defines configuration for RoboBottom Bots."""

    FORCE_TESTMODE = True
    """Force testmode app-wide. Will add "- testmode" in some places to indicate that the bot is running in testmode.
    - `None` &nbsp;&nbsp;→ Don't force either option, True for Windows, False for other OSes
    - `True` &nbsp;&nbsp;→ Always run in testmode
    - `False` → Never run in testmode
    """

    STATUS = hikari.Status.capitalize
    """Discord status (Online, Idle, etc.)"""

    ACTIVITY: ActivityTD | None = {
      'name': 'Testing...',  # ' - Testmode' will be added here if enabled
      'type': hikari.ActivityType.PLAYING,
      'state': None,
      'url': None,
    }
    """Discord activity (Watching X, Playing Y, etc.)"""

if True:  # \/ # Constants
  TOKEN = tcr.get_token('TOKEN.txt', depth=3)  # 3-1 = 2 counting src/
  TESTMODE = (os.name == 'nt') if S.FORCE_TESTMODE is None else S.FORCE_TESTMODE

if True:  # \/ # Sync Functions

  def testmode() -> str:
    return ' - testmode' if TESTMODE else ''

if True:  # \/ # Async Functions

  async def get_guild_count():
    return len(await BOT.rest.fetch_my_guilds())

if True:  # \/ # Rich tracebacks
  if testmode():
    from rich.traceback import install as install_tb

    install_tb()

if True:  # \/ # Validate & Modify Settings (e.g. add ' - testmode' to activity)
  if True:  # \/ # FORCE_TESTMODE
    if S.FORCE_TESTMODE not in (_it := (None, True, False)):
      raise RBSettingsError('S.FORCE_TESTMODE must be either of: ', _it)
    S.FORCE_TESTMODE = bool(S.FORCE_TESTMODE)

  if True:  # \/ # STATUS
    if S.STATUS not in (
      _it := (
        hikari.Status.ONLINE,
        hikari.Status.IDLE,
        hikari.Status.DO_NOT_DISTURB,
        hikari.Status.OFFLINE,
      )
    ):
      raise RBSettingsError('S.STATUS must be either of: ', _it, force_no_indent=0, let_no_indent=0)

  if True:  # \/ # ACTIVITY
    if not (S.ACTIVITY is None or isinstance(S.ACTIVITY, dict)):
      raise RBSettingsError('S.ACTIVITY must be either None or dict')
    if not tcr.able(hikari.Activity, **S.ACTIVITY):
      raise RBSettingsError(
        'Invalid S.ACTIVITY configuration. '
        "Check hikari.Activity's arguments for proper config, got: \n",
        S.ACTIVITY,
        force_no_indent=False,
      )
    S.ACTIVITY['name'] += testmode()
    S.ACTIVITY = hikari.Activity(**S.ACTIVITY)

if True:  # \/ # Bot
  BOT = hikari.GatewayBot(token=TOKEN, banner=None)
  MCL = miru.Client(BOT)
  ACL = arc.GatewayClient(BOT)
  tasks.load(BOT)

if True:  # \/ # Events

  @BOT.listen(hikari.StartingEvent)
  async def onStartingEvent(event: hikari.StartingEvent): ...

  @BOT.listen(hikari.StartedEvent)
  async def onStartedEvent(event: hikari.StartedEvent): ...

  @BOT.listen(hikari.StoppingEvent)
  async def onStoppingEvent(event: hikari.StoppingEvent): ...

  @BOT.listen(hikari.StoppedEvent)
  async def onStoppedEvent(event: hikari.StoppedEvent): ...


if True:  # \/ # Run
  BOT.run(status=S.STATUS, activity=S.ACTIVITY)
