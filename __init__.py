import os
import pathlib as p
import sys

from tcrutils.console import c

if sys.version_info[:2] < (_ := (3, 12)):
	required = ".".join(str(x) for x in _)
	you_have = ".".join(str(x) for x in sys.version_info[:3])  # :3

	msg = f"This bot requires Python {required} or newer (You have {you_have})"
	print(msg)
	raise SystemExit(1)

if True:  # sys.path extension, needed due to modularity issue.
	# This is reflected in vscode path settings.
	_ = p.Path(__file__).parent
	sys.path.insert(0, str(_.absolute()))
	sys.path.insert(0, str((_ / "common").absolute()))
	sys.path.insert(0, str((_ / "src").absolute()))

import rb
