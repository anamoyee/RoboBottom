import datetime
import pathlib as p
from collections.abc import Callable
from typing import Any, NotRequired, Unpack
from typing import TypedDict as TD

import hikari
import pytz
import r01_types as m_types
import tcrutils as tcr
from colored import Back, Fore, Style

# from r01_types import *


class ActivityTD(TD):
  name: str
  type: NotRequired[Unpack[hikari.ActivityType]]
  state: NotRequired[str | None]
  url: NotRequired[str | None]


class CreatedByTD(TD):
  id: int
  name: str


class S:
  """Defines configuration for RoboBottom."""

  NO: str = ':x:'
  """'Something failed or could not be completed or an error occured' emoji/prefix."""
  YES: str = ':white_check_mark:'
  """'Something was completed successfully' emoji/prefix."""
  WARN: str = ':warning:'
  """'No error occured but something went slightly wrong OR nothing happened due to your actions but you are notified of it' emoji/prefix."""

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

  DB_DIRECTORY_BACKUP: p.Path = DB_DIRECTORY.with_name(f'{DB_DIRECTORY.name}2')
  """The directory where the database backups are stored."""

  MAX_BACKUPS_BEFORE_DELETING_OLDEST: int = 31  # A month of backups should be enough (assuming the default backup chron of backup once every 24 hours)
  """If this amount of backups is present, the oldest backup will be deleted to not take so much disk space. TO NOT DELETE ANY BACKUPS SET THIS TO 0 - WARNING: your disk may fill up - each backup is a complete copy!"""

  BACKUP_CRON: str = '0 0 * * *'  # default: Take a backup once every day at midnight
  """The cron schedule for taking a backup of the entire database.

  For more info see:
  - https://arc.hypergonial.com/api_reference/utils/loops/#arc.utils.loops.CronLoop (hikari-arc is the library this bot uses)
  - https://en.wikipedia.org/wiki/Cron
  """

  BACKUP_DIRECTORY_NAME_FORMAT: str = '%Y-%m-%d_%H%M'
  """How each of the backups' respective folders should be named. Example: 2022-03-18_0000.

  Seconds are shifted by 30 seconds forward due to the fact that the cron scheduler somehow starts the function a bit early so it registers as sth like 23:59:59 the previous day so i just chopped off the seconds so it's not visible.
  """

  GLOBAL_TIMEZONE: datetime.tzinfo = pytz.timezone('Europe/Warsaw')
  """The global timezone used for global events in need of coordination, like backups. Also a default timezone for users."""

  USER_BACKUP_EXPORT_FILENAME: str = '{author_id}_{datetime:%Y-%m-%d_%H%M}_robobockup.json'
  """The file which user receives when they export their data.

  Available placeholders:
  - `{author_id}` (str)
  - `{author_username}` (str)
  - `{datetime}` (datetime.datetime)
  """

  USER_BACKUP_COOLDOWN: int = 15 * 60  # 15 minutes
  """How many seconds have to pass between usages of /backup export for the same user for it to succeed."""

  MIN_REMINDER_TIME: int = 15  # seconds
  """The minimum time a reminder has to be scheduled for to be accepted. Otherwise an error is shown to the user."""

  MAX_REMINDER_TIME_IN_TIMEOUT: int = 60 * 1  # seconds
  """The maximum time a reminder's timeout can be set to, if higher the reminder is instead moved to archive. Timeout is set when the reminder fails to be sent repeatedly."""

  BANNER: str | None = p.Path('assets/txt/banner.txt')  # Default: assets/txt/banner.txt
  """The banner ascii that is shown when the bot launches. Just edit the banner.txt file. When set to None, both this banner and the hikari default banner are not shown."""

  BANNER_COLORS: tuple[str, str] = (
    Style.RESET + Fore.DARK_GRAY,
    Style.RESET + Fore.ORANGE_1 + Style.BOLD,
  )
  """This tuple is available under the name BC while editing the banner.txt file to add colors.

  You may alternatively not use it and directly input Fore.WHITE + Syle.BOLD, etc. etc. every time but it's cumbersome"""

  EMBED_COLORS: dict[str, int] = {
    'colon': 0xFF8000,
    'polaris': 0x00FF80,
    'primary': 0x00BFFF,
    'settings': 0xFF8000,
    'secondary': 0x8000FF,
    'reminder': 0xFFFF00,
    'cancelled': 0xFF0000,
    'archive': 0x808080,
    'error': 0xFF0000,
    'success': 0x00FF00,
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

  RANDOM_SURES: list[str] = list({
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
  })  # fmt: skip
  """Displays in the above prompt (if you choose so or leave the default value)."""

  SORTKEY: Callable[[m_types.Reminder], Any] = lambda r: -r.unix  # Default: sort by time of expiry, reversed: lambda r: -r.unix
  """Defines how the reminders are sorted in the internal reminder list. This affects how they are displayed and which indices they occupy (used in cancelling)."""

  REMINDER_TASK_INTERVAL_SECONDS: int = 1 - 0.0069  # Default: 1 (with correction)
  """Interval for the function that sends reminders when they expire."""

  APOLOGISE_FOR_INCONVENIENCE_AFTER_EXPIRED_FOR: int = 30  # seconds
  """If reminder wasnt delivered within this many seconds after it expired, it'll contain a footer explaining the delay and apologising for the inconvenience."""

  REMINDER_EXPIRED_FOOTER = 'Sorry for sending this reminder {expired_for} too late! >.<'
  """See above."""

  REMINDER_EMBED: dict[str, Any] = {
    'title': '🔔 Reminder!',
    # Do not specify 'description'!! The reminder's body takes up description and it cannot be overriden.
    'color': EMBED_COLORS['reminder'],
  }
  """The box with a (usually yellow) stripe on the right telling you that your reminder has expired. The whole point of the bot actually..."""

  REMINDER_LIST_EMBED: dict[str, Any] = {
    'title': 'Your reminders ({amount})',
    'color': EMBED_COLORS['secondary'],
  }
  """Same as one above, just for the list of reminders, not a single reminder (usually accessed with a `'.'` or `'list'`)."""

  REMINDER_LIST_REMINDERS_PER_PAGE: int = 24
  """Number of reminders per page in the reminder list."""

  REMINDER_LIST_MAX_CHARS_PER_REMINDER: int = (tcr.discord.DiscordLimits.Embed.DESCRIPTION_SAFE - (5 * REMINDER_LIST_REMINDERS_PER_PAGE)) // REMINDER_LIST_REMINDERS_PER_PAGE
  """Number of characters a single reminder can take until it's cut off with an elipsis."""

  REMINDER_LIST_MAX_TOTAL_REMINDERS_PER_USER: int = REMINDER_LIST_REMINDERS_PER_PAGE * 10  # 10 pages should be MORE THAN ENOUGH...
  """Number of reminders a user can have in total."""

  NAVBAR_LABEL: dict[str, str] = {
    'prev': '<< Page {page}',
    'next': 'Page {page} >>',
  }
  """Labels for the navigation buttons."""

  PRINT_REVOLUTION: bool = True
  """Nice if you get the reference. If this is True, the bot on startup prints the revolution "On the eve of our {} revolution..." (aka the how many times this bot has booted up without changing versions)."""

  ACCIDENTAL_SUFFIXES: set[str] = {"'", '\\', ']'}
  """Those characters will be ignored if left at the end of an input string.

  For example:
  ```15m test'```
  Will be interpreted as:
  ```15m test```

  This is to prevent accidental:
  - ugly text if present at the end of the reminder text
  - syntax errors if present at the end of the reminder delay

  when pressing the enter key to send the message.
  """

  SUSPICIOUS_RIPPLE_CANCEL_TIME = 3 * 60  # 3 minutes
  """If user uses a `fuck` command after this amount of time after scheduling their most recent reminder, they will be prompted to confirm this action."""

  ARCHIVE_SUFFIX: str = '@'
  """Character used after the command name to signify its target to be the archive list.

  - `c1` == cancel the first reminder
  - `c&1` == remove the first reminder from the archive
  """

  FORCE_TESTMODE = None  # Default: None
  """[DEV] Force testmode app-wide. Will add "- Testmode" in some places to indicate that the bot is running in testmode.
  - `None` &nbsp;&nbsp;→ Don't force either option, True for Windows, False for other OSes
  - `True` &nbsp;&nbsp;→ Always run in testmode
  - `False` → Never run in testmode
  """

  DEV_IDS: tuple[hikari.Snowflake] = (
    507642999992352779,
  )  # This manages permissions, not credits, for example user that's NOT on that list CAN'T invoke commands, but /botstatus uses a separate entry, look lower on this list of settings
  """[DEV] A list of discord IDs of user accounts that are permitted to invoke developer functions (dangerous!)"""

  DEFAULT_EANBLED_GUILDS: tuple[hikari.Snowflake] | None = None  # (1145433323594842166,) # Default: None
  """[DEV] The guilds' IDs in which the slash commands would be updated quicker, for development purposes only.

  To enable slash commands on all guilds set it to () or None"""

  DEV_EANBLED_GUILDS: tuple[hikari.Snowflake] | None = (1145433323594842166,)  # Default: None
  """[DEV] The guilds' IDs in which the developer slash commands are enabled.

  To enable dev commands on all guilds set it to () or None (NOT RECOMMENDED)."""

  DEV_ERROR_CHANNEL: hikari.Snowflake | None = 1254892313981751296
  """[DEV] The channel for any unhandled errors will appear on this channel as a red embed. Set this to None to disable this feature (all errors will be silently ignored)."""

  ### The following settings should not be modified.

  CREATED_BY: CreatedByTD = {'id': 507642999992352779, 'name': 'anamoyee'}  # Do not change or confusion will ensue (if a bug is ever triggered)
  """Should not be changed - my discord name & ID. This is rarely used to refer a user that stumbled upon a bug to me so i can fix it. This is also used in one line in credits."""
  CREATED_BY_STR: str = f"@{CREATED_BY['name']} (discord_id={CREATED_BY['id']})"
  """See above."""

  MAJOR_VERSION_TEMPLATE: str = '2.1.%s'
  """The non-patch versions are not incremented automatically on `$ cmp`"""
