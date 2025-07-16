from collections.abc import Callable
from typing import TYPE_CHECKING, Self

import arc
from mods._.config import S
from mods._.db import UserDB

from ..models import Reminder

if TYPE_CHECKING:
	from ..db import RbProfile


@arc.utils.interval_loop(seconds=1)
async def send_reminder_loop():
	for dbkey in UserDB.keys():  # noqa: SIM118
		with UserDB(dbkey) as user:
			for prof in user.profiles:
				prof: RbProfile
				for rem in list(prof.reminders):
					if rem.is_due():
						try:
							await rem.send(
								Reminder.RemindDisplay(
									dbkey=dbkey,
									user=user,
									prof=prof,
								)
							)
						finally:
							prof.reminders.remove(rem)
