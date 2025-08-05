import asyncio

from common import ACL, BOT
from hikari import TextableChannel
from mods._.config import S as S1
from mods._.tools import OPTION_EPHEMERAL, ephemeral_from_bool
from mods.rb.tools import try_fetch_channel_from_str
from prelude import *

from ..config import S
from ..lang import LANG


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.peek"))
async def cmd_peek(
	ctx: arc.GatewayContext,
	amount: arc.Option[int, arc.IntParams(**LANG.get_arc_command("/.peek:amount"), min=1, max=10)] = 7,
	channel_str: arc.Option[str | None, arc.StrParams(**LANG.get_arc_command("/.peek:channel"))] = None,
	ephemeral: OPTION_EPHEMERAL = True,
) -> None:
	try:
		channel: TextableChannel = await try_fetch_channel_from_str(
			channel_str,
			author=ctx.author,
			here_channel=ctx.channel,
			guild=ctx.get_guild(),
		)
	except RuntimeError:
		await ctx.respond(LANG.get_arc(ctx, "/.peek:channel.invalid_channel"), flags=hikari.MessageFlag.EPHEMERAL)
		return

	flags = ephemeral_from_bool(ephemeral)

	await ctx.defer(flags=flags)

	embeds = await (
		channel.fetch_history()
		.limit(3 * amount)  # sanity check - dont let the user make a spammer out of the bot
		.filter(
			lambda msg, __bot_id=BOT.get_me().id: msg.author.id == __bot_id,
			lambda msg: len(msg.embeds) == 1,
		)
		.limit(amount)
		.reversed()
		.map(lambda msg: msg.embeds[0])
		# this looks so pretty, big thanks to whoever made hikari.LazyIterator <3
	)

	if not embeds:
		await ctx.respond(LANG.get_arc(ctx, "/.peek.no_embeds"), flags=flags)
		return

	try:
		await ctx.respond(embeds=embeds, flags=flags)
	except Exception:
		await ctx.respond(LANG.get_arc(ctx, "/.peek.failed_to_send"), flags=flags)
