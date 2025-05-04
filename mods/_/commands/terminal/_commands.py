from prelude import *
from tcrutils.void import alambda

from . import commands
from ._base import (
	TerminalCommand,
	TerminalCommandCallback,
	TerminalCommandCallbackResult,
	TerminalCommandCategory,
	TerminalOtherResponse,
	_resolve_cmd_aliases_in_place_and_return,
	_resolve_dict_aliases_in_place_and_return,
)
from ._base import TerminalCommand as Cmd

terminal_command_categories = {
	"cards": TerminalCommandCategory(name="Cards", emoji="🎴"),
	"fun": TerminalCommandCategory(name="Fun", emoji="💎"),
	"fusions": TerminalCommandCategory(name="Fusions", emoji="🔀"),
	"programs": TerminalCommandCategory(name="Programs", emoji="💻"),
	"system": TerminalCommandCategory(name="System", emoji="⚙️"),
	"tools": TerminalCommandCategory(name="Tools", emoji="🛠️"),
}

TERMINAL_COMMANDS = {
	"random": commands.random,
	"yes": commands.yes,
	"help": commands.help,
	"zoo": {
		None: Cmd(
			displayname="zoo",
			description="Base command for zoo",
			usage=["zoo [args?]"],
			callback=alambda(lambda *args, **_: f"zoo base command executed with args={args}"),
		),
		"a": Cmd(
			displayname="a",
			description='Handles the "a" subcommand of "zoo"',
			usage=["zoo a [args?]"],
			callback=alambda(lambda *args, **_: f"zoo a command executed with args={args}"),
		),
		"b": Cmd(
			displayname="b",
			description='Handles the "b" subcommand of "zoo"',
			usage=["zoo b [args?]"],
			callback=alambda(lambda *args, **_: f"zoo b command executed with args={args}"),
		),
		"c": "b",
	},
	"z": "zoo",
}


def count_leaf_values_of_dict(d: dict) -> int:
	count = 0
	for value in d.values():
		if isinstance(value, dict):
			count += count_leaf_values_of_dict(value)
		elif not isinstance(value, str):  # Do not count aliases
			count += 1
	return count


_total_commands_loaded_right_now = count_leaf_values_of_dict(TERMINAL_COMMANDS)

_resolve_cmd_aliases_in_place_and_return(TERMINAL_COMMANDS)
_resolve_dict_aliases_in_place_and_return(TERMINAL_COMMANDS)
