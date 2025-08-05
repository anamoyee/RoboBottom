from collections.abc import Callable

import hikari
import hikari.channels
from common import BOT


async def try_fetch_channel_from_str(
	s: str | None,
	/,
	author: hikari.User,
	guild: hikari.GatewayGuild | None = None,
	here_channel: hikari.PartialChannel | None = None,
	*,
	predicate: Callable[[hikari.PartialChannel], bool] = lambda ch: isinstance(ch, hikari.TextableChannel),
) -> hikari.PartialChannel:
	"""If `s is None`, fetch the user's DM channel, otherwise try to find an accessible channel most simillar to `s`. If no channel can be found, raise RuntimeError.

	Note: by default the predicate is set to only textable channels, if you need all channels or different set of channels change the predicate.
	"""

	if s is None or s.lower() == "dm":
		channel = await author.fetch_dm_channel()

		if predicate(channel):
			return channel

	if s == "here" and here_channel is not None:
		channel = here_channel

		if predicate(channel):
			return channel

	if s.isdigit():
		try:
			n = int(s)  # Note, try is required as stuff like superscript isdigit for some reason but is not int-able
		except ValueError:
			pass
		else:
			channel = await BOT.rest.fetch_channel(n)

			if predicate(channel):
				return channel

	if guild is not None:
		for channel in guild.get_channels().values():
			if (channel.name.casefold() == s.casefold().lstrip("#")) and predicate(channel):
				return channel

	raise RuntimeError("Unable to find a suitable channel")
