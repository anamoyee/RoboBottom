import hikari
import tcrutils as tcr
from tcrutils import c

from .. import commands, db, events, models, templates
from ..bot import BOT
from ..settings import S


@BOT.listen()
async def on_started(event: hikari.StartedEvent):
	if S.RUNTIME_FLAGS.SHELL:
		tcr.start_eval_session()
