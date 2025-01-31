import arc

from ..bot import ACL


@ACL.include
@arc.slash_command("botstatus")
async def cmd_botstatus(ctx: arc.Context):
	await ctx.respond("botstatus")
