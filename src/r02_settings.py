from r01_types import *


class S:
  """Defines configuration for RoboBottom."""

  FORCE_TESTMODE = None  # Default: None
  """Force testmode app-wide. Will add "- Testmode" in some places to indicate that the bot is running in testmode.
  - `None` &nbsp;&nbsp;→ Don't force either option, True for Windows, False for other OSes
  - `True` &nbsp;&nbsp;→ Always run in testmode
  - `False` → Never run in testmode
  """

  STATUS = hikari.Status.ONLINE
  """Discord status (Online, Idle, etc.)"""

  ACTIVITY: ActivityTD | None = {
    'name': 'Testing...',  # ' - Testmode' will be added here if enabled
    'type': hikari.ActivityType.CUSTOM,
    'state': None,
    'url': None,
  }
  """Discord activity (Watching X, Playing Y, etc.)"""

  DB_DIRECTORY: p.Path = p.Path.home() / 'CCLocalReminders'  # Default: ~/CCLocalReminders
  """Pathlib Path object represending the directory where all user reminders are stored as subdirectories with the name of their discord ID. Created automatically if it doesn't exist."""

  BANNER: str | None = (p.Path(__file__).parent.parent / 'banner.txt').read_text().strip()  # Default: ../banner.txt
  """The banner ascii that is shown when the bot launches. Just edit the banner.txt file. When set to None, both this banner and the hikari default banner are not shown."""

  BANNER_COLORS: tuple[int, str, str] = (
    36,  # Default: 36 for default banner.txt
    attr(0) + fg('dark_gray'),
    attr(0) + fg('orange_1') + attr('bold'),
  )
  """Colors of the above banner.

  1st item: int, The cutoff point
  2nd item: str, The color before cutoff
  3rd item: str, The color after cutoff

  Banner is split into lines, every line is split at the cutoff mark. Characters before the cutoff (on the left) are colored color[1], characters after it are colored color[2]
  """

  EMBED_COLORS: dict[str, int] = {
    'colon': 0xFF8000,
    'polaris': 0x00FF80,
    'primary': 0x00BFFF,
    'settings': 0xFF8000,
    'secondary': 0x8000FF,
    'reminder': 0xFFFF00,
    'error': 0xFF0000,
  }
  """Defines the color of the stripe on the left side of each embed from that category.

  Valid formats:
  - Int (`0xff8000` or `16744448`)
  - 0xStr (`"0xff8000"`)
  - #Str (`"#ff8000"`)
  """

  SCHEDULED_SUCCESSFULLY_PROMPT: str = "🔔 **{random_sure}** I'll remind you in **{time}**"
  """This string is displayed after a reminder was successfully scheduled.

  For example:
  > 1h test
  > **Got it!** I'll remind you in **1 hour**
  """

  RANDOM_SURES: list[str] = list(
    {  # list(set(x)) is used to prevent duplicates. Replace list(set()) with [] to allow duplicates - They will effectively have higher chance to be displayed.
      'Done!',
      'Got it!',
      'Sweet!',
      'Awesome!',
      'Great!',
      'Roger!',
      'Epic!',
      'Gotcha!',
      'Noted!',
      'Sure thing!',
      'Sounds good!',
      'Heck yeah!',
      'All done!',
    }
  )
  """Displays in the above prompt (if you choose so or leave the default value)."""

  SORTKEY: Callable[[Reminder], Any] = lambda reminder: -reminder.unix  # Default: sort by time of expiry, reversed: lambda r: -r.unix
  """Defines how the reminders are sorted in the internal reminder list. This affects how they are displayed and which indices they occupy (used in cancelling)."""

  REMINDER_TASK_INTERVAL_SECONDS: int = 1 - 0.0069  # Default: 1 (with correction)
  """Interval for the function that sends reminders when they expire."""

  REMINDER_EMBED = {
    'title': '🔔 Reminder!',
    # Do not specify 'description'!! The reminder's body takes up description and it cannot be overriden.
    'color': EMBED_COLORS['reminder'],
  }
  """The box with a (usually yellow) stripe on the right telling you that your reminder has expired. The whole point of the bot actually..."""

  NAVBAR_LABEL: dict[str, str] = {
    'prev': '<< Page {page}',
    'next': 'Page {page} >>',
  }
  """Labels for the navigation buttons."""

  DEV_IDS: tuple[tcr.discord.Snowflake] = (507642999992352779,)
  """[DEV] A list of discord IDs of user accounts that are permitted to invoke developer functions (dangerous!)"""

  DEFAULT_EANBLED_GUILDS: tuple[tcr.discord.Snowflake] | None = None  # (1145433323594842166,) # Default: None
  """[DEV] The guilds' IDs in which the slash commands would be updated quicker, for development purposes only.

  To enable slash commands on all guilds set it to () or None"""

  DEV_EANBLED_GUILDS: tuple[tcr.discord.Snowflake] | None = (1145433323594842166,)  # Default: None
  """[DEV] The guilds' IDs in which the developer slash commands are enabled.

  To enable dev commands on all guilds set it to () or None (NOT RECOMMENDED)."""

  DEBUG_REMINDERS_ON_SEND: bool = True
  """[DEV] Provide additional information in the console about reminders being triggered and the state of the reminder_task"""
