from pathlib import Path as _Path

from prelude import get_logger

from .machinery import LANG, POOLS, LangImportError, LangImportExecError, LangImportMissingOrMalformedOutputVariableError, merge_directory, merge_directory_and_log

logger = get_logger(__name__)

merge_directory_and_log(LANG, _Path(__file__).parent / "_lang", logger.info)
merge_directory_and_log(POOLS, _Path(__file__).parent / "_pools", logger.info, ("language pool", "language pools"))
