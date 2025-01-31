import sys

import arguably

if __package__ is None:
	import pathlib as p

	msg = "\x1b[1;91m" "Unable to run outside of package context. Use this command instead:" f"{sys.executable} -m src.{p.Path(__file__).stem}" "\x1b[0m"

	print(msg)
	exit(1)


@arguably.command
def __root__(*, shell: bool = False):
	if not arguably.is_target():
		return

	from . import commands, events
	from .bot import BOT
	from .settings import S

	S.RUNTIME_FLAGS.SHELL = shell

	BOT.run(
		status=S.INITIAL_PRESENCE.STATUS,
		activity=S.INITIAL_PRESENCE.ACTIVITY,
	)


from .version import __appname__, __version__

arguably.run(
	name=__appname__,
	version_flag=("-v", "--version"),
)
