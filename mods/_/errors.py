import traceback
from dataclasses import dataclass as _dataclass

from tcrutils import discord_ifys as IFYs
from tcrutils.codeblock import codeblocks
from tcrutils.extract_error import extract_error, extract_traceback

from common.bot import ACL, BOT
from common.errors import ThisError
from prelude import *

from .config import S


class ModError(ThisError):
	"""Common base class for all errors coming from mods."""


class UserGetsDetailsError(ModError):
	"""Any error happend but also user gets to see an error message if this isnt caught. This is supposed to be subclassed since user also gets to see this errors `.__class__.__name__`. If this class is not subclassed, the class name will not be shown (annonymous error type).

	You can disable this functionality `'_'`-mod-wide in the config.
	"""

	user_details: str
	"""The details given to the user."""

	display_class_name: bool = True
	"""When a class inherits from UserGetsDetailsError and is raised: whether to display its name or just 'Error!'. (The details are still displayed)"""

	def __init__(self, /, user_details: str, *, display_class_name: bool = True) -> None:
		self.user_details = user_details
		self.display_class_name = display_class_name
		super().__init__(user_details)

	def display_to_user(self) -> str:
		"""Return the error message to display to the user."""

		if self.__class__ is UserGetsDetailsError:  # No fish? No pass
			base_message = self.user_details
		else:
			base_message = f"**{self.__class__.__name__ if self.display_class_name else 'Error'}!** {self.user_details}"

		return base_message  # Not returning directly, in case of coding in any extra details, like base_message += 'to report this bug...' or whatever


@ACL.set_error_handler
async def handle_uncaught_errors(ctx: arc.GatewayContext, e: BaseException) -> None:
	if S.ENABLE_USER_GETS_DETAILS_ERRORS and isinstance(e, UserGetsDetailsError):
		await ctx.respond(e.display_to_user())
	else:
		await ctx.respond("**Error!**")  # If the error is not of type UserGetsDetailsError, dont give details.

	if S.ERROR_CHANNEL:
		msg = f"## Unhandled command error in `{ctx.command.display_name}` triggered by {IFYs.userify(ctx.author.id)}\n" + codeblocks(
			extract_error(e),
			extract_traceback(e),
			langcodes=("py", "py"),
			max_length=1800,
		)

		await BOT.rest.create_message(S.ERROR_CHANNEL, msg)

	raw_msg = f"Unhandled command error in {ctx.command.display_name!r} triggered by {ctx.author.id}"
	c.error(raw_msg)

	traceback.print_exception(type(e), e, e.__traceback__)
