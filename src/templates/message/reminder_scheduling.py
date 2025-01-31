import datetime as _datetime
import random as _rng

from .. import pool as _pool


def successful(
	expires_at: _datetime.datetime,
) -> dict:
	return {
		"content": f"🔔 **{_rng.choice(tuple(_pool.SURES))}** I'll remind you in **{expires_at}**",
	}
