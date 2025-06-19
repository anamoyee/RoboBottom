from datetime import datetime, timezone

from _.config.settings import Author
from tcrutils.decorator import instance as _instance

from .emoji import CustomEmojiStatic
from .models import *


@_instance  # "S = S()", but with correct typhints, works on the latest pylance vscode extension version as of the time of writing this sentence
class S(BM):
	"""Represents the settings of the functional part of the reminder bot."""

	AUTHOR: Author = Author(discord_id=507642999992352779, discord_username="anamoyee")

	### Submenus ############################################################################################################################################################

	EMOJI: CustomEmojiStatic = {}
	COLOR: ColorPaletteStatic = {}
