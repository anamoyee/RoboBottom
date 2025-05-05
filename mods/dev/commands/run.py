from contextlib import ExitStack

from _._version import __version__
from _.db import GlobalDB, GuildDB, UserDB, VersionDB
from _.tools import OPTION_EPHEMERAL, ephemeral_from_bool
from tcrutils.codeblock import codeblock, discord_exception
from tcrutils.console import c
from tcrutils.print import fmt_iterable

from prelude import *

from ._base import GROUP_DEV


@GROUP_DEV.include
@arc.slash_subcommand("run", "Run a command in the mysterious... Python interpreter!")
async def cmd_dev_run(
	ctx: arc.GatewayContext,
	code: arc.Option[str, arc.StrParams("The code to run")],
	do_await: arc.Option[bool, arc.BoolParams("Await the result if prompted to?", name="await")] = True,
	do_exec: arc.Option[bool, arc.BoolParams("Use exec() instead of eval(). _ var is return value", name="exec")] = False,
	ephemeral: OPTION_EPHEMERAL = True,
	open_this_user: arc.Option[bool, arc.BoolParams('Open my user\'s writable database record as a variable "user"?')] = True,
	open_this_version: arc.Option[bool, arc.BoolParams('Open current version\'s writable database record as a variable "version"?')] = True,
	open_this_guild: arc.Option[bool, arc.BoolParams('Open current guilds\'s writable database record as a variable "guild" (if applicable)?')] = True,
	open_global: arc.Option[bool, arc.BoolParams('Open the global writable database record as a variable "global_"?')] = True,
):
	if do_await:
		awaitable, code = code.startswith("await "), code.removeprefix("await ")

	try:
		with ExitStack() as stack:
			d = {}

			if open_this_user:
				d["user"] = stack.enter_context(UserDB(ctx.user.id))
			if open_this_version:
				d["version"] = stack.enter_context(VersionDB(__version__))
			if open_this_guild and ctx.guild_id:
				d["guild"] = stack.enter_context(GuildDB(ctx.guild_id))
			if open_global:
				d["global_"] = stack.enter_context(GlobalDB())

			if do_exec:
				exec(code, globals(), d)
				result = d.get("_")
			else:
				result = eval(code, globals(), d)

		if do_await and awaitable:
			result = await result
	except Exception as e:
		result = e
		errored = True
	else:
		errored = False

	out = discord_exception(result) if errored else codeblock(fmt_iterable(result), langcode="py")

	await ctx.respond(out, flags=ephemeral_from_bool(ephemeral))
