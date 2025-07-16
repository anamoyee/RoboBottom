from typing import TYPE_CHECKING, Any

from mods._.events import DatabaseInitEvent
from prelude import *

from .. import models


def mixin_RbProfile():
	"""Should be only called once. Mixes in RbProfile to the root Profile class, should be stackable (should be able to be used by other mods simultaneously)."""
	global RbProfile

	from _.db import model_profile

	##################################################################

	class RbProfile(model_profile.Profile):
		reminders: list[models.Reminder] = pd.Field(default_factory=list)

		def sort_reminders(self):
			self.reminders.sort(key=models.Reminder.sort_key)

	##################################################################

	model_profile.Profile = RbProfile

	return RbProfile


if TYPE_CHECKING:

	class RbProfile(mixin_RbProfile()): ...

	# only valid after mixin_RbProfile is called


@DatabaseInitEvent.subscribe
async def on_database_init(event: DatabaseInitEvent):
	mixin_RbProfile()
