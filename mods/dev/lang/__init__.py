from pathlib import Path

from _.lang import LANG, merge_directory_and_log
from prelude import *

merge_directory_and_log(
	LANG,
	Path(__file__).parent / "_lang",
	get_logger(__name__).info,
)
