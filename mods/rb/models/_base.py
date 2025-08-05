from enum import Flag as _BaseFlag
from enum import StrEnum, auto
from functools import reduce
from typing import Self

from _.models._base import Object
from prelude import *


class StrFlag(_BaseFlag):
	NONE: Self

	def __init_subclass__(cls) -> None:
		try:
			cls.NONE  # noqa: B018
		except AttributeError as e:
			raise RuntimeError(f"{cls.__name__}.NONE is required (add NONE = 0 to {cls.__name__} class declaration)") from e

		return super().__init_subclass__()

	@classmethod
	def all(cls) -> Self:
		result = cls(0)
		for flag in cls:
			result |= flag
		return result

	@classmethod
	def make_symbol_associations(cls) -> dict[Self, str]:
		return {}

	@classmethod
	def _checked_make_symbol_associations(cls) -> dict[Self, str]:
		dct = cls.make_symbol_associations()

		if (missing := (cls.all() ^ reduce(lambda a, b: a | b, [cls.NONE, *dct]))) != cls.NONE:  # noqa: FURB118
			raise RuntimeError(f"{cls.__name__}.make_symbol_associations: missing symbol association for: {missing.name}")

		if len(dct.values()) != len(set(dct.values())):
			raise RuntimeError(f"{cls.__name__}.make_symbol_associations: duplicate symbol association: {dct}")

		return dct

	@classmethod
	def from_str(cls, s: str, /) -> Self:
		symbols = cls._checked_make_symbol_associations()

		symbols_inv = {v: k for k, v in symbols.items()}

		result = cls.NONE

		for symbol_str in s:
			try:
				result |= symbols_inv[symbol_str]
			except KeyError as e:
				raise ValueError(f"{cls.__name__}.from_str: invalid symbol: {symbol_str}") from e

		return result

	@classmethod
	def from_str_prefix(cls, s: str, /) -> tuple[Self, str]:
		symbols = cls._checked_make_symbol_associations()
		symbols_inv = {v: k for k, v in symbols.items()}

		result = cls.NONE

		i = 0
		while i < len(s):
			symbol_str = s[i]
			try:
				result |= symbols_inv[symbol_str]
				i += 1
			except KeyError:
				break

		return result, s[i:]

	def __str__(self) -> str:
		symbols = self._checked_make_symbol_associations()

		return "".join(symbols[flag] for flag in self)
