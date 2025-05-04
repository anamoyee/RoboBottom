import random
from abc import ABC
from collections.abc import Hashable

import arc

from prelude import ZooBM, pd

from ..tools import make_loopback_channel_link


class GetByHashSet[T](set[T]):
	"""A custom set class that allows retrieval of items by their name."""

	def __getitem__(self, key: Hashable) -> T:
		name_hash = hash(key)

		for item in self:
			if hash(item) == name_hash:
				return item

		raise KeyError(key)

	def get[Default](self, key: Hashable, default: Default = None) -> T | Default:
		"""Retrieve an item from the set by its name using hash comparison, if not found return the default."""

		try:
			return self[key]
		except KeyError:
			return default


def HashEq_by(attr_name: str):
	"""Make this class instances compatible with sets and dictionaries by using the given attribute as a hashable."""

	def decorator[Type: type](cls: Type) -> Type:
		def __hash__(self):
			return hash(getattr(self, attr_name))

		def __eq__(self, other):
			if not isinstance(other, self.__class__):
				return False
			return getattr(self, attr_name) == getattr(other, attr_name)  # Other hasattr attr_name since it's the same class and pydantic ensures that the attr exists and is valid

		cls.__hash__ = __hash__
		cls.__eq__ = __eq__
		return cls

	return decorator


if True:  # Bases

	class Object(ZooBM, ABC):
		"""Common base class for all Zoo objects (like: items, animals, leaders, etc.)."""


if True:  # complex-ish object attribute provider ABCs

	class HasEmoji(Object, ABC):
		"""Represents a Zoo object with an emoji field."""

		emoji: str
		"""The emoji of this object. May be a unicode emoji or a markdown emoji ('<:emoji_name:emoji_id>')."""

		def is_emoji_unicode(self) -> bool:
			"""Return True, if this EmojidObject's emoji is a unicode emoji, else return False."""

			return ":" not in self.emoji
