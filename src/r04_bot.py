from r03_constants import *

if True:  # Bot
  BOT = hikari.GatewayBot(token=TOKEN, banner=('hikari' if S.BANNER is not None else None))
  MCL = miru.Client(BOT)
  ACL = arc.GatewayClient(BOT, default_enabled_guilds=S.DEFAULT_EANBLED_GUILDS or hikari.UNDEFINED)
  tasks.load(BOT)
