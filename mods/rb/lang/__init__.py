from pathlib import Path as _Path

from _.lang import *
from _.lang.machinery import merge_directory_and_log
from prelude import get_logger

logger = get_logger(__name__)

merge_directory_and_log(LANG, _Path(__file__).parent / "_lang", logger.info)
merge_directory_and_log(POOLS, _Path(__file__).parent / "_pools", logger.info, ("language pool", "language pools"))
