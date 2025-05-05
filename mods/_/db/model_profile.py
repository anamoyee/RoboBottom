import random as rng
from collections import defaultdict
from collections.abc import Iterable
from enum import StrEnum
from typing import TYPE_CHECKING

from prelude import *

from ..models import HashEq_by


class ProfileID(StrEnum):
	"""An ID to differenciate multiple profiles on a single account while also being able to target/select them.

	Variants prefixed with `_` are considered 'restricted', that means they will not be chosen as a candidate for `ProfileID.get_random()`.
	"""

	_ROBO = 'robo'  # fmt: skip # The robo profile is 100% 'not needed' in this rewrite since the whole point of there being profiles from the start makes it pointless, however i couldn't have just left it out!!
	_KITSUNE = "kitsune"

	if True:  # Common Animals
		OX = "ox"
		DOG = "dog"
		FLY = "fly"
		PIG = "pig"
		CAT = "cat"
		BAT = "bat"
		COW = "cow"
		FOX = "fox"
		DUCK = "duck"
		CRAB = "crab"
		FISH = "fish"
		FROG = "frog"
		BEAR = "bear"
		DOVE = "dove"
		WORM = "worm"
		SEAL = "seal"
		MOUSE = "mouse"
		SLOTH = "sloth"
		HIPPO = "hippo"
		SHEEP = "sheep"
		SKUNK = "skunk"
		SQUID = "squid"
		SNAIL = "snail"
		KOALA = "koala"
		CHICK = "chick"
		WHALE = "whale"
		ZEBRA = "zebra"
		HORSE = "horse"
		CAMEL = "camel"
		RABBIT = "rabbit"
		LIZARD = "lizard"
		BEAVER = "beaver"
		PARROT = "parrot"
		SPIDER = "spider"
		SHRIMP = "shrimp"
		BEETLE = "beetle"
		TURKEY = "turkey"
		GORILLA = "gorilla"
		LEOPARD = "leopard"
		PENGUIN = "penguin"
		CHICKEN = "chicken"
		GIRAFFE = "giraffe"
		SNOWMAN = "snowman"
		HAMSTER = "hamster"
		CRICKET = "cricket"
		ELEPHANT = "elephant"
		DINOSAUR = "dinosaur"
		HEDGEHOG = "hedgehog"
		CROCODILE = "crocodile"
		CATERPILLAR = "caterpillar"

	@classmethod
	def get_random(cls, excluded: Iterable["ProfileID"] = ()) -> "ProfileID":
		"""Get a random ProfileID enum variant, excluding those in `excluded`.

		Raise a ValueError when excluded contains all available ProfileIDs.
		"""
		restricted_union_excluded = {member for member in cls if member.name.startswith("_")}.union(excluded)

		if not set(cls).difference(restricted_union_excluded):
			raise ValueError("Unable to get a new ProfileID due to none being available (all non-restricted ProfileIDs were provided as `excluded`).")

		while (chosen := cls(rng.choice(list(cls)))) in restricted_union_excluded:
			pass

		return chosen


@HashEq_by("id")
class Profile(RbBM):
	id: ProfileID
	"""The ProfileID of this profile, that is: `fox`, `cat`, `kitsune`, etc. encapsulated in a StrEnum."""
