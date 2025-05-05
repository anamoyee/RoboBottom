from datetime import date, datetime, time, timedelta

from prelude import *

from ..config import S


class Version(RbBM):
	current_revolution: int = 0
	last_boot_datetime: datetime = pd.Field(default_factory=lambda: datetime.now(tz=S.TZINFO))
