from datetime import datetime, timedelta, timezone

from tcrutils.decorator import instance as _instance

from .emoji import CustomEmojiStatic
from .models import *


@_instance  # "S = S()", but with correct typhints, works on the latest pylance vscode extension version as of the time of writing this sentence
class S(BM):
	"""Represents the main, shared settings of the entire bot itself, not only the `'_'` mod, since the builtin mod is always 'depended on' by other mods (hardcoded) (that means, you can access it through other mods) it can be used as a bot-wide config, though read-only. This is for looking up values to other mods, not storing values that are relevant only in your mod. For this make your own config in your mod, kind of like this one."""

	AUTHOR: Author = Author(discord_id=507642999992352779, discord_username="anamoyee")
	"""Author of the `'_'` mod, effectivelly myself, the author of the bot itself."""

	### Submenus ############################################################################################################################################################

	EMOJI: CustomEmojiStatic = {}
	"""Custom emojis used by the `'_'` mod."""

	COLOR: ColorPaletteStatic = {}
	"""Represents the color palette for the bot."""

	FILE: HikariFileStatic = {}
	"""Represents the hikari file palette for the bot."""

	### Consts ##############################################################################################################################################################

	NO: str = "❌"
	"""'Something failed or could not be completed or an error occured' emoji/prefix."""
	YES: str = "✅"
	"""'Something was completed successfully' emoji/prefix."""
	WARN: str = "⚠️"
	"""'No error occured but something went slightly wrong OR nothing happened due to your actions but you are notified of it' emoji/prefix."""

	TZINFO: timezone = datetime.now().astimezone().tzinfo  # By default, the current machine's local timezone
	"""Timezone used by the bot whenever the `datetime` module needs it."""

	DB_DIRECTORY: p.Path = p.Path("~/CCLocalReminders").expanduser()
	"""The directory where the database is stored."""
	DB_DIRECTORY.mkdir(parents=True, exist_ok=True)

	MIRU_TIMEOUT: int | float | timedelta | None = 60
	"""The argument supplied to miru `View`s (and `ext.Menu`s) when asked for a timeout

	- setting this to None will make views never time out automatically
	- setting this to a float or int will be interpreted as amount of seconds.
	- this can also be timedelta
	"""

	### Permissions #########################################################################################################################################################

	PERMISSION_DENIED_ERROR_IS_MEGU_BUTTON_PNG: bool = True
	"""When sending a message informing the user they should not press someone else's button send /mods/_/assets/megu_button.png instead."""

	### Error Handling ######################################################################################################################################################

	ENABLE_USER_GETS_DETAILS_ERRORS: bool = True
	"""When this setting is set to True, any uncaught arc-originating errors inheriting from `UserGetsDetailsError` will be shown to the user with the provided details. If not, any erorrs of this type or subtype will be treated as any other errors."""

	ERROR_CHANNEL: hikari.Snowflake | None = None
	"""When an error is unhandled, send an error report to this channel. If not set, no error report will be sent (only shown in the console)."""
