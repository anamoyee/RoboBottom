from collections.abc import Awaitable, Callable
from enum import Enum
from enum import auto as _enum_auto

from prelude import *

from ...config import S
from ...errors import UserGetsDetailsError


class TerminalCommandReturnedInvalidResponseError(UserGetsDetailsError): ...


type TerminalCommandCallback = Callable[..., Awaitable[TerminalCommandCallbackResult]]
type TerminalCommandCallbackResult = str | dict | hikari.Embed | TerminalOtherResponse


class TerminalOtherResponse(Enum):
	UNKNOWN_COMMAND = _enum_auto()
	APPLICATION_DID_NOT_RESPOND = _enum_auto()
	NO_COMMAND_PROVIDED = _enum_auto()


class TerminalCommandCategory(ZooBM):
	name: str
	emoji: str

	def __str__(self) -> str:
		return f"{self.emoji} {self.name}"


class TerminalCommand(ZooBM):
	callback: TerminalCommandCallback
	"""The async function that will provide this command's functionality and/or response."""
	displayname: str
	"""That's how the command will be displayed in `$ help`. This does not affect its lookup, that is controlled by the command dictionary."""
	description: str | None = pd.Field(default=None)
	"""The description of this command in `$ help`.

    If None, the `$ help` command will say it doesn't have any info on this command / this command doesnt exit (TODO: <-- find out which one exactly has been implemented for this )"""

	category: TerminalCommandCategory | None = pd.Field(default=None)
	"""Help Menu: If provided, this command will be displayed under this category in the help menu. If not, it will be hidden from the help menu (secret command.)"""
	usage: list[str] = pd.Field(default_factory=list)
	"""Help Menu: What arguments are needed for this command?"""
	example: list[str] = pd.Field(default_factory=list)
	"""Help Menu: Usage examples for this command"""
	aliases: list[str] = pd.Field(default_factory=list)
	"""Help Menu: Other aliases for this command

    NOTE: This field gets filled with aliases during the alias resolving process.
    """

	def __call__(self, *args: str, **kwargs) -> Awaitable[TerminalCommandCallbackResult]:
		return self.callback(*args, **kwargs)

	def help_embed(self) -> hikari.Embed | None:
		if self.description is None:
			return None

		em = hikari.Embed(
			title=f"$ {self.displayname}",
			description=self.description,
			color=S.COLOR.PRIMARY,
		)

		if self.usage:
			em.add_field(name="Usage", value="\n".join(f"`$ {x}`" for x in self.usage), inline=True)

		if self.example:
			em.add_field(name="Examples", value="\n".join(f"`$ {x}`" for x in self.example), inline=True)

		if self.aliases:
			em.set_footer(f"Aliases: {', '.join(self.aliases)}")

		return em


def _resolve_cmd_aliases_in_place_and_return(d: dict):
	for _, value in list(d.items()):
		if isinstance(value, TerminalCommand):
			for alias in value.aliases:
				d[alias] = value
		elif isinstance(value, dict):
			_resolve_cmd_aliases_in_place_and_return(value)


def _resolve_dict_aliases_in_place_and_return[K, V](d: dict[K, V | str]) -> dict[K, V]:
	keys_to_resolve = []

	for key, value in d.items():
		if isinstance(value, str):
			keys_to_resolve.append((key, value))
		elif isinstance(value, dict):
			_resolve_dict_aliases_in_place_and_return(value)

	for key, alias in keys_to_resolve:
		if alias in d:
			d[key] = d[alias]

			if isinstance(d[key], TerminalCommand):
				d[key].aliases.append(key)
			elif isinstance(d[key], dict) and None in d[key] and isinstance(d[key][None], TerminalCommand):
				d[key][None].aliases.append(key)
		else:
			raise ValueError(f"Alias '{alias}' not found in the same scope")

	return d


def get_terminal_command(commands: dict[str, TerminalCommand | dict], part: str, /, *parts: str) -> tuple[TerminalCommand | None, tuple[str]]:
	"""Get a command from the commands dict and any extra arguments if any."""
	if part in commands:
		if isinstance(commands[part], TerminalCommand):
			return commands[part], parts
		elif not parts:
			if None in commands[part]:
				cmd = commands[part][None]
				return cmd, ()
			else:
				return None, ()
		else:
			return get_terminal_command(commands[part], *parts)
	elif None in commands:
		return commands[None], (part, *parts)
	else:
		return None, ()
