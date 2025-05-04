import os
import pathlib as p
import sys

from tcrutils.console import c

if os.name != "nt":  # Optimize for Unix systems
	import asyncio

	import uvloop

	asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if sys.version_info[:2] < (_ := (3, 12)):
	required = ".".join(str(x) for x in _)
	you_have = ".".join(str(x) for x in sys.version_info[:3])  # :3

	msg = f"Zoo requires Python {required} or newer (You have {you_have})"
	c.error(msg)
	exit(1)

if True:  # sys.path extension, needed due to modularity issue.
	# This is reflected in vscode path settings.
	_ = p.Path(__file__).parent
	sys.path.insert(0, str(_.absolute()))
	sys.path.insert(0, str((_ / "common").absolute()))
	sys.path.insert(0, str((_ / "src").absolute()))

import src.zoo
