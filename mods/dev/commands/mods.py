from _.tools import OPTION_EPHEMERAL, OPTION_TO_FILE, dump_respond

from mod_loader import MODS
from prelude import *

from ._base import GROUP_DEV


@GROUP_DEV.include
@arc.slash_subcommand("mods", "View the list of currently loaded mods.")
async def cmd_dev_objects_items(
	ctx: arc.GatewayContext,
	ephemeral: OPTION_EPHEMERAL = True,
	to_file: OPTION_TO_FILE = False,
) -> None:
	await dump_respond(
		*MODS.items(),
		ctx=ctx,
		ephemeral=ephemeral,
		to_file=to_file,
	)
