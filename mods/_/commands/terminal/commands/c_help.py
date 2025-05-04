from ....db import UserDB
from .. import _commands as m_commands
from .._base import *
from .._base import TerminalCommand as Cmd


async def _help_list(*, ctx: arc.GatewayContext, **_) -> TerminalCommandCallbackResult:
	user_id = 507642999992352779

	with UserDB(user_id) as acc:
		if not acc.has_selected_profile():
			await acc.create_profile(owner=user_id)
		await acc.create_profile(owner=user_id)

		acc.selected_profile.name += "!"

		return repr(acc)


async def _help_specific(cmd_name: str, /, **_) -> TerminalCommandCallbackResult:
	command, _ = get_terminal_command(m_commands.TERMINAL_COMMANDS, cmd_name)

	if command is None or (em := command.help_embed()) is None:
		return {"content": f"ERROR: command {cmd_name!r} not found.", "flags": hikari.MessageFlag.EPHEMERAL}

	return em


async def _help(*args: str, **ctxs) -> TerminalCommandCallbackResult:
	if args:
		return await _help_specific(args[0], **ctxs)
	else:
		return await _help_list(**ctxs)


help = Cmd(
	callback=_help,
	displayname="help",
	description="Lists most terminal commands, or provides info on a specific one.",
	usage=["help [command?]"],
	example=["help help"],
	aliases=["cmds", "commands", "h", "list"],
)
