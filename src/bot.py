import arc
import hikari
import miru
from tcrdiscord import get_token

from .settings import S

BOT = hikari.GatewayBot(
	token=get_token(S.CREDENTIALS.TOKEN_FILENAME),
)

ACL = arc.GatewayClient(BOT)
MCL = miru.Client(BOT)
