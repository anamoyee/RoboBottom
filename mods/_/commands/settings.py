from miru.ext import menu

from common import ACL, MCL
from prelude import *

from .._version import __version__
from ..lang import LANG
from ..view.settings import SettingsMainScreen


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.settings"))
async def cmd_settings(ctx: arc.GatewayContext) -> None:
	menu_ = menu.Menu()

	builder = await menu_.build_response_async(MCL, SettingsMainScreen(menu_, ctx))

	await ctx.respond_with_builder(builder)

	MCL.start_view(menu_)
