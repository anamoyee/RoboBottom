from _.tools import OPTION_EPHEMERAL, ephemeral_from_bool
from common import zoo
from prelude import *
from tcrutils.codeblock import codeblock
from tcrutils.print import fmt_iterable

from ._base import GROUP_DEV as __GROUP_DEV

GROUP_DEV_OBJECTS = __GROUP_DEV.include_subgroup("objects", "View read-only states of objects, like items, animals, leaders, etc.")


def display_objects_as_codeblock(objects) -> str:
	return codeblock(fmt_iterable(objects), langcode="py")


# TODO: since zoo.objects was removed, reimpl this
# for attr_name in zoo.objects.model_fields:

# 	@GROUP_DEV_OBJECTS.include
# 	@arc.slash_subcommand(attr_name, f"View read-only state of {attr_name}.")
# 	async def cmd_dev_objects_items(
# 		ctx: arc.GatewayContext,
# 		ephemeral: OPTION_EPHEMERAL = True,
# 		attr_name=attr_name,
# 	) -> None:
# 		await ctx.respond(
# 			display_objects_as_codeblock(getattr(zoo.objects, attr_name)),
# 			flags=ephemeral_from_bool(ephemeral),
# 		)
