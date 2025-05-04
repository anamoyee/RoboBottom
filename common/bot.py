from prelude import *
from prelude import __TOKEN

BOT = hikari.GatewayBot(token=__TOKEN)  # , banner=('hikari' if S.BANNER is not None else None))
MCL = miru.Client(BOT)
ACL = arc.GatewayClient(
	BOT,
	invocation_contexts=[
		hikari.ApplicationContextType.GUILD,
		hikari.ApplicationContextType.BOT_DM,
		hikari.ApplicationContextType.PRIVATE_CHANNEL,
	],
)  # , default_enabled_guilds=S.DEFAULT_EANBLED_GUILDS or hikari.UNDEFINED)
