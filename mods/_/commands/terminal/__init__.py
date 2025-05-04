from common import ACL, zoo
from tcrutils.iterable import cut_at

from ...lang import LANG
from ._base import *
from ._commands import TERMINAL_COMMANDS, _total_commands_loaded_right_now

TERMINAL_COMMAND_STR_BANNED_CHARACTERS_REPLACEMENTS: dict[str, str] = {
	"`": "'",
}
"""Defines a mapping for replacing substrngs of /terminal command:<this> into any string: 1, 0, or any number of characters long, though usually 1 or 0.

### Example:
`{"`": "'"}`
- **IN:**  "haha let me just break the codeblock formatting by inputting a ` backtick hehe >:3"
- **OUT:** "$ haha let me just break the codeblock formatting by inputting a ' backtick hehe >:3"
"""

logger = get_logger(__name__)


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.terminal"))
async def cmd_terminal(
	ctx: arc.GatewayContext,
	command_str: arc.Option[str, arc.StrParams(**LANG.get_arc_command("/.terminal:command"), max_length=256)],
) -> None:
	# 1. Split & Filter

	for char, replacement in TERMINAL_COMMAND_STR_BANNED_CHARACTERS_REPLACEMENTS.items():
		command_str = command_str.replace(char, replacement)

	command_str_parts = command_str.split(" ")

	# 2. Get command

	if not command_str:
		response = TerminalOtherResponse.NO_COMMAND_PROVIDED
	else:
		command, argv = get_terminal_command(TERMINAL_COMMANDS, *command_str_parts)

		# 3. Run command

		if command is None:
			response = TerminalOtherResponse.UNKNOWN_COMMAND
		else:
			ctxs = {
				"ctx": ctx,
				"command": command,
				"command_str": command_str,
				"command_str_filtered": command_str,
				"sysargv0": command_str_parts[: len(argv) - 1],
			}

			response = await command(*argv, **ctxs)

	# 4. Respond (if and how requested by the command)

	if response == TerminalOtherResponse.APPLICATION_DID_NOT_RESPOND:
		return

	bash_header = f"`{cut_at(f'$ {command_str}', n=69)}`"  # LOLL it actually is 69 (with the '$ '), i counted.
	# NOTE: due to my cut_at implementation it works slightly differnetly when it's on the edge of cutting it off but it's good enough...

	if response == TerminalOtherResponse.UNKNOWN_COMMAND:
		await ctx.respond(f"{bash_header}\n**{command_str[:128]}**: command not found")  # 128 - again, i counted exactly
		return
	if isinstance(response, dict):
		await ctx.respond(**response)
		return
	if isinstance(response, hikari.Embed):
		await ctx.respond(content=bash_header, embed=response)
		return
	if isinstance(response, str):
		await ctx.respond(f"{bash_header}\n{response}")
		return

	# 5. If response was invalid, raise an error and let it be handled by printing to the user

	raise TerminalCommandReturnedInvalidResponseError(user_details="A terminal command returned an invalid response.")


logger.info(f"Loaded {_total_commands_loaded_right_now} base terminal commands.")
