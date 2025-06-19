from common import ACL, BOT
from prelude import *

from ..config import S
from ..lang import LANG


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.remind"))
async def cmd_remind(ctx: arc.GatewayContext) -> None:
	await ctx.respond("wip")
