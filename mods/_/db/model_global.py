from datetime import datetime

from prelude import *

from ..config import S


class Global(RbBM):
	banned_snowflakes: set[int] = pd.Field(default_factory=set)
	last_boot_datetime: datetime = pd.Field(default_factory=lambda: datetime.now(tz=S.TZINFO))
