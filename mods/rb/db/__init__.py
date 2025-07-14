from typing import TYPE_CHECKING, Any

from mods._.events import DatabaseInitEvent
from prelude import *


def mixin_RbProfile():
	"""Should be only called once. Mixes in RbProfile to the root Profile class, should be stackable (should be able to be used by other mods simultaneously)."""
	global RbProfile

	from _.db import model_profile

	##################################################################

	class RbProfile(model_profile.Profile):
		reminders: list[str] = pd.Field(default_factory=list)

		def test_method(self):
			return f"test from: {self.display_name=}"

	##################################################################

	model_profile.Profile = RbProfile

	return RbProfile


if TYPE_CHECKING:

	class RbProfile(mixin_RbProfile()): ...

	# only valid after mixin_RbProfile is called


@DatabaseInitEvent.subscribe
async def on_database_init(event: DatabaseInitEvent):
	mixin_RbProfile()
