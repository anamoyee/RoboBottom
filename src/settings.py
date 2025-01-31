from pathlib import Path

import hikari
import pydantic as pd

from .models import BM


class SettingsCredentials(BM):
	TOKEN_FILENAME: str = "TOKEN.txt"


class SettingsInitialPresence(BM):
	STATUS: str = hikari.Status.ONLINE
	ACTIVITY: hikari.Activity = hikari.Activity(name="nya")


class SettingsDatabase(BM):
	ROOT_DIR: Path = Path.home() / "CCLocalReminders4"


class SettingsRuntimeFlags(BM):
	SHELL: bool = False


class Settings(BM):
	CREDENTIALS: SettingsCredentials = {}
	INITIAL_PRESENCE: SettingsInitialPresence = {}
	DATABASE: SettingsDatabase = {}

	RUNTIME_FLAGS: SettingsRuntimeFlags = {}


S = Settings()
