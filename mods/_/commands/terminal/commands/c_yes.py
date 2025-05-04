from .._base import *
from .._base import TerminalCommand as Cmd


async def _yes(*args: str, **_) -> TerminalCommandCallbackResult:
	max_len = 1800

	word = " ".join(args) or "y"

	text = ""

	while (len(text) + len(word) + 1) < max_len:
		text += f"\n{word}"

	return text.strip()


yes = Cmd(
	callback=_yes,
	displayname="yes",
	description="I... don't even know how to explain this one.\nhttps://en.wikipedia.org/wiki/Yes_(Unix)",
	usage=["yes [message]"],
)
