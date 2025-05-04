import random as rng
from collections import defaultdict
from collections.abc import Iterable
from enum import StrEnum
from typing import TYPE_CHECKING

from prelude import *

from ..models import Animal, HashEq_by

if TYPE_CHECKING:
	from _.commands.rescue import Rescue


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


# class _ProfileTerminal(ZooBM):
# 	"""Represents the terminal-related data of this profile."""

# 	unlocked: bool = False
# 	"""Whether or not this profile has unlocked the terminal."""
# 	admin: bool = False
# 	"""Whether or not this profile has unlocked the terminal administrator access via the `$ adminunlock` command."""
# 	commands_found: list[str] = pd.Field(default_factory=list)
# 	"""All top-level (non-nested) terminal commands found, for example `zoo`, not `zoo goals`, `zoo items`, the unlocked command for both is `zoo`, the top level command."""
# 	mechanic_points: int = 0
# 	"""Amount of murphy points this profile contains."""
# 	fishy: _ZooTerminalFishy | None = None
# 	"""Info about the `$ fishy` minigame of this profile."""
# 	garden: _ZooTerminalGarden | None = None
# 	"""Info about the `$ garden` of this profile."""
# 	cards: _ZooTerminalCards | None = None
# 	"""Info about the cards of this profile."""
# 	fusion: _ZooTerminalFusion | None = None
# 	"""Info about the fusions & NFBs of this profile."""


class ProfileSettings(ZooBM):
	"""Represents the settings of this profile."""

	private: bool = False


@HashEq_by("id")
class Profile(ZooBM):
	id: ProfileID
	"""The ProfileID of this profile, that is: `fox`, `cat`, `kitsune`, etc. encapsulated in a StrEnum."""
	name: str
	"""Zoo name of this profile."""

	def set_name(self, name: str) -> None:
		self.name = name

	settings: ProfileSettings = {}

	animals: defaultdict[str, int] = pd.Field(default_factory=lambda: defaultdict(int))

	def fetch_owned_animals(self) -> dict[str, tuple[Animal, int]]:
		return {animal_name: (Animal.from_name(animal_name), count) for (animal_name, count) in self.animals.items()}

	# terminal: _ProfileTerminal = {}

	async def apply_rescue(self, rescue: "Rescue") -> None:
		self.animals[rescue.animal.name] += 1 if not rescue.is_pair else 2
