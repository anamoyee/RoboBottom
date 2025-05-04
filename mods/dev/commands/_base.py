from _.config import S as RootS

from common import ACL
from prelude import *

from ..config import S


async def dev_only_hook(ctx: arc.GatewayContext) -> arc.HookResult:
	"""Aborts execution if user is not authorised to run dev commands. Notifies user by responding."""
	if ctx.author.id not in S.DEV_IDS:
		await ctx.respond(f"{RootS.NO} You are not allowed to use this command.", flags=hikari.MessageFlag.EPHEMERAL)
		return arc.HookResult(abort=True)
	return arc.HookResult()


GROUP_DEV = ACL.include_slash_group(
	"dev",
	"Developer cmdlets",
	autodefer=arc.AutodeferMode.EPHEMERAL,
	guilds=S.DEV_GUILDS,
	default_permissions=hikari.Permissions.ADMINISTRATOR,
	invocation_contexts=[
		hikari.ApplicationContextType.GUILD,
		# hikari.ApplicationContextType.BOT_DM,
		# hikari.ApplicationContextType.PRIVATE_CHANNEL,
	],
)

GROUP_DEV.add_hook(dev_only_hook)
