import arc

from ._ import GROUP


@GROUP.include
@arc.slash_subcommand("debug")
async def cmd_debug(ctx: arc.Context):
	await ctx.respond("debug")
