from datetime import datetime

from tcrutils.sdb2 import ShelfManager, SingleShelfManager

from prelude import *

from .._version import __version__
from ..config import S
from .model_global import Global
from .model_guild import Guild
from .model_profile import Profile, ProfileID
from .model_user import User
from .model_version import Version


class UserDB(ShelfManager[User]):
	PATH = S.DB_DIRECTORY / "users"

	def default_factory(self) -> str:
		return User()


class GuildDB(ShelfManager[Guild]):
	PATH = S.DB_DIRECTORY / "guilds"

	def default_factory(self) -> str:
		return Guild()


class VersionDB(ShelfManager[Version]):
	PATH = S.DB_DIRECTORY / "versions"

	def default_factory(self):
		return Version()


class GlobalDB(SingleShelfManager[Global]):
	PATH = S.DB_DIRECTORY / "global"

	def default_factory(self):
		return Global()


# Initialize the global and current verion's DBs
with GlobalDB() as dbglobal, VersionDB(__version__) as dbversion:
	dbversion.current_revolution += 1
	dbversion.last_boot_datetime = datetime.now(tz=S.TZINFO)

	dbglobal.last_boot_datetime = dbversion.last_boot_datetime
