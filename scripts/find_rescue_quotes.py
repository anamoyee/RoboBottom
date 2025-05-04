import datetime
import pathlib as p
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import Literal

import dcx_pd as dcx
from tcrutils.console import c


def add_placeholders_to_quote(q: str) -> str:
	return q  # todo


def fixdisplay_set(set_: set) -> str:
	repr_ = repr(set_)

	if repr_ == "set()":
		return repr_

	return repr_[:-1] + ",}"


@dataclass
class AnimalC:
	name: str
	displayname: str
	emoji: str
	rare: bool

	def __str__(self):
		return f"ANIMAL_{self.name.upper().replace('-', '').replace(' ', '_')} := Animal(name={self.name!r}, displayname={self.displayname!r}, emoji={self.emoji!r},)"


ANIMALS = [
	ANIMAL_BAT := AnimalC(
		name="bat",
		displayname="Bat",
		emoji="🦇",
		rare=False,
	),
	ANIMAL_BEAR := AnimalC(
		name="bear",
		displayname="Bear",
		emoji="🐻",
		rare=False,
	),
	ANIMAL_BEAVER := AnimalC(
		name="beaver",
		displayname="Beaver",
		emoji="🦫",
		rare=False,
	),
	ANIMAL_BEETLE := AnimalC(
		name="beetle",
		displayname="Beetle",
		emoji="🪲",
		rare=False,
	),
	ANIMAL_CAMEL := AnimalC(
		name="camel",
		displayname="Camel",
		emoji="🐪",
		rare=False,
	),
	ANIMAL_CAT := AnimalC(
		name="cat",
		displayname="Cat",
		emoji="🐱",
		rare=False,
	),
	ANIMAL_CATERPILLAR := AnimalC(
		name="caterpillar",
		displayname="Caterpillar",
		emoji="🐛",
		rare=False,
	),
	ANIMAL_CHICK := AnimalC(
		name="chick",
		displayname="Chick",
		emoji="🐥",
		rare=False,
	),
	ANIMAL_CHICKEN := AnimalC(
		name="chicken",
		displayname="Chicken",
		emoji="🐔",
		rare=False,
	),
	ANIMAL_COW := AnimalC(
		name="cow",
		displayname="Cow",
		emoji="🐄",
		rare=False,
	),
	ANIMAL_CRAB := AnimalC(
		name="crab",
		displayname="Crab",
		emoji="🦀",
		rare=False,
	),
	ANIMAL_CRICKET := AnimalC(
		name="cricket",
		displayname="Cricket",
		emoji="🦗",
		rare=False,
	),
	ANIMAL_CROCODILE := AnimalC(
		name="crocodile",
		displayname="Crocodile",
		emoji="🐊",
		rare=False,
	),
	ANIMAL_DEER := AnimalC(
		name="deer",
		displayname="Deer",
		emoji="🦌",
		rare=False,
	),
	ANIMAL_DINOSAUR := AnimalC(
		name="dinosaur",
		displayname="Dinosaur",
		emoji="🦕",
		rare=False,
	),
	ANIMAL_DOG := AnimalC(
		name="dog",
		displayname="Dog",
		emoji="🐶",
		rare=False,
	),
	ANIMAL_DOVE := AnimalC(
		name="dove",
		displayname="Dove",
		emoji="🕊️",
		rare=False,
	),
	ANIMAL_DUCK := AnimalC(
		name="duck",
		displayname="Duck",
		emoji="🦆",
		rare=False,
	),
	ANIMAL_ELEPHANT := AnimalC(
		name="elephant",
		displayname="Elephant",
		emoji="🐘",
		rare=False,
	),
	ANIMAL_FISH := AnimalC(
		name="fish",
		displayname="Fish",
		emoji="🐟",
		rare=False,
	),
	ANIMAL_FLY := AnimalC(
		name="fly",
		displayname="Fly",
		emoji="🪰",
		rare=False,
	),
	ANIMAL_FOX := AnimalC(
		name="fox",
		displayname="Fox",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_FROG := AnimalC(
		name="frog",
		displayname="Frog",
		emoji="🐸",
		rare=False,
	),
	ANIMAL_GIRAFFE := AnimalC(
		name="giraffe",
		displayname="Giraffe",
		emoji="🦒",
		rare=False,
	),
	ANIMAL_GORILLA := AnimalC(
		name="gorilla",
		displayname="Gorilla",
		emoji="🦍",
		rare=False,
	),
	ANIMAL_HAMSTER := AnimalC(
		name="hamster",
		displayname="Hamster",
		emoji="🐹",
		rare=False,
	),
	ANIMAL_HEDGEHOG := AnimalC(
		name="hedgehog",
		displayname="Hedgehog",
		emoji="🦔",
		rare=False,
	),
	ANIMAL_HIPPO := AnimalC(
		name="hippo",
		displayname="Hippo",
		emoji="🦛",
		rare=False,
	),
	ANIMAL_HORSE := AnimalC(
		name="horse",
		displayname="Horse",
		emoji="🐴",
		rare=False,
	),
	ANIMAL_KOALA := AnimalC(
		name="koala",
		displayname="Koala",
		emoji="🐨",
		rare=False,
	),
	ANIMAL_LEOPARD := AnimalC(
		name="leopard",
		displayname="Leopard",
		emoji="🐆",
		rare=False,
	),
	ANIMAL_LIZARD := AnimalC(
		name="lizard",
		displayname="Lizard",
		emoji="🦎",
		rare=False,
	),
	ANIMAL_MOUSE := AnimalC(
		name="mouse",
		displayname="Mouse",
		emoji="🐭",
		rare=False,
	),
	ANIMAL_OX := AnimalC(
		name="ox",
		displayname="Ox",
		emoji="🐂",
		rare=False,
	),
	ANIMAL_PARROT := AnimalC(
		name="parrot",
		displayname="Parrot",
		emoji="🦜",
		rare=False,
	),
	ANIMAL_PENGUIN := AnimalC(
		name="penguin",
		displayname="Penguin",
		emoji="🐧",
		rare=False,
	),
	ANIMAL_PIG := AnimalC(
		name="pig",
		displayname="Pig",
		emoji="🐷",
		rare=False,
	),
	ANIMAL_RABBIT := AnimalC(
		name="rabbit",
		displayname="Rabbit",
		emoji="🐰",
		rare=False,
	),
	ANIMAL_SEAL := AnimalC(
		name="seal",
		displayname="Seal",
		emoji="🦭",
		rare=False,
	),
	ANIMAL_SHEEP := AnimalC(
		name="sheep",
		displayname="Sheep",
		emoji="🐑",
		rare=False,
	),
	ANIMAL_SHRIMP := AnimalC(
		name="shrimp",
		displayname="Shrimp",
		emoji="🦐",
		rare=False,
	),
	ANIMAL_SKUNK := AnimalC(
		name="skunk",
		displayname="Skunk",
		emoji="🦨",
		rare=False,
	),
	ANIMAL_SLOTH := AnimalC(
		name="sloth",
		displayname="Sloth",
		emoji="🦥",
		rare=False,
	),
	ANIMAL_SNAIL := AnimalC(
		name="snail",
		displayname="Snail",
		emoji="🐌",
		rare=False,
	),
	ANIMAL_SPIDER := AnimalC(
		name="spider",
		displayname="Spider",
		emoji="🕷️",
		rare=False,
	),
	ANIMAL_SQUID := AnimalC(
		name="squid",
		displayname="Squid",
		emoji="🦑",
		rare=False,
	),
	ANIMAL_TURKEY := AnimalC(
		name="turkey",
		displayname="Turkey",
		emoji="🦃",
		rare=False,
	),
	ANIMAL_WHALE := AnimalC(
		name="whale",
		displayname="Whale",
		emoji="🐳",
		rare=False,
	),
	ANIMAL_WORM := AnimalC(
		name="worm",
		displayname="Worm",
		emoji="🪱",
		rare=False,
	),
	ANIMAL_ZEBRA := AnimalC(
		name="zebra",
		displayname="Zebra",
		emoji="🦓",
		rare=False,
	),
]

export = dcx.Export.from_path(p.Path(__file__).parent / "gitignored/zoo-bot@9tbh.json")


@dataclass
class Processed:
	emoji: str
	verb: str
	an: Literal["an", "a"] | None
	pair: bool
	animal: str | None
	quote: str

	def __post_init__(self):
		self.quote = self.quote.strip()

		self.quote = add_placeholders_to_quote(self.quote)

		self.pair = bool(self.pair)

		if self.pair:
			self.emoji = self.emoji[:1]

			self.an = None
			self.animal = None

	def to_animal2(self) -> "AnimalC2":
		_animals1 = [x for x in ANIMALS if x.emoji == self.emoji]

		if len(_animals1) != 1:
			raise RuntimeError("len(animals1) != 1")

		animal1 = _animals1[0]

		return AnimalC2(
			name=animal1.name,
			displayname=animal1.displayname,
			emoji=self.emoji,
			rare=animal1.rare,
			an=self.an == "an",
			rescue_quotes={self.quote} if not self.pair else set(),
			rescue_pair_quotes={self.quote} if self.pair else set(),
			rescue_verbs={self.verb},
		)


@dataclass
class AnimalC2(AnimalC):
	an: bool
	rescue_verbs: set[str]
	rescue_quotes: set[str]
	rescue_pair_quotes: set[str]

	def __str__(self):
		return f"ANIMAL_{self.name.upper().replace('-', '').replace(' ', '_')} := AnimalC(name={self.name!r}, displayname={self.displayname!r}, emoji={self.emoji!r}, an={self.an!r}, rescue_verbs={{}}, rescue_quotes={fixdisplay_set(self.rescue_quotes)}, rescue_pair_quotes={fixdisplay_set(self.rescue_pair_quotes)},)"

	def merge(self, other: "AnimalC2") -> "AnimalC2":
		return AnimalC2(
			name=self.name,
			displayname=self.displayname,
			emoji=self.emoji,
			rare=self.rare,
			an=self.an,
			rescue_verbs=self.rescue_verbs | other.rescue_verbs,
			rescue_quotes=self.rescue_quotes | other.rescue_quotes,
			rescue_pair_quotes=self.rescue_pair_quotes | other.rescue_pair_quotes,
		)

	@classmethod
	def merge_all(cls: type["AnimalC2"], animals: list["AnimalC2"]) -> list["AnimalC2"]:
		"""Merge all animals with the same emoji."""
		grouped_animals: dict[str, list[AnimalC2]] = defaultdict(list)

		for animal in animals:
			grouped_animals[animal.emoji].append(animal)

		return [reduce(lambda a, b: a.merge(b), group) for group in grouped_animals.values()]


processedes: list[Processed] = []


def is_april_fools_range(dt: datetime.datetime) -> bool:
	return datetime.date(dt.year, 3, 31) <= dt.date() <= datetime.date(dt.year, 4, 2)


for message in export.messages:
	if message.author.id != 1008563327380766812:
		continue

	if not message.content:
		continue

	if not any(message.content.startswith(a.emoji) for a in ANIMALS):
		continue

	first_line = message.content.split("\n")[0]

	if first_line.count(" ") < 3:
		continue

	if "+" in first_line and "->" in first_line:
		continue

	if "Purchased" in first_line:
		continue

	if "The fusion was successful" in first_line:
		continue

	if "Thank you for everything <3" in first_line:
		continue

	if "Trade completed" in first_line:
		continue

	if "Mystery Chick" in first_line:
		continue

	if "This server currently has" in first_line:
		continue

	if "you can rescue another animal in" in first_line:
		continue

	if "is trading" in first_line:
		continue

	if "**Your animals were unfused!**" in first_line:
		continue

	if is_april_fools_range(message.timestamp):  # skip pokemon stuff throwing off the search
		continue

	first_line = first_line.removesuffix(" 🍀")

	# first_line = re.sub(r"(you have \d+)$", "", first_line)
	PATT = re.compile(r"^(?P<emoji>.{1,2}) You (?P<verb>\D+?) (?P<an>a|an) (?P<pair>pair of )?\*\*(?P<animal>\D+?)\*\*! (?:🎲 )?(?P<quote>[^\(]+)(?:\(you have \d+\))?$", re.RegexFlag.I | re.RegexFlag.U)

	t0 = time.perf_counter()

	m = PATT.match(first_line)

	t1 = time.perf_counter()
	elapsed = datetime.datetime.fromtimestamp(t1, tz=datetime.UTC) - datetime.datetime.fromtimestamp(t0, tz=datetime.UTC)

	if not m:
		c.warn("huh?: " + repr(first_line))
		continue

	processedes.append(Processed(**m.groupdict()))

c(len(processedes))

generated = [x.to_animal2() for x in processedes]

merged = AnimalC2.merge_all(generated)

sorted_ = sorted(merged, key=lambda x: x.name)

for animal2 in sorted_:
	print(animal2, end=",\n")

c(len(sorted_))

from tcrutils.print import print_iterable

print_iterable(reduce(lambda x, y: x | y, [x.rescue_verbs for x in sorted_]))  # noqa: FURB118

c({x.name: len(x.rescue_verbs) for x in sorted_})
c({x.name: len(x.rescue_pair_quotes) for x in sorted_})
c({x.name: len(x.rescue_quotes) for x in sorted_})

c({x.name: len(x.rescue_verbs) for x in sorted_ if not len(x.rescue_verbs)})
c({x.name: len(x.rescue_pair_quotes) for x in sorted_ if not len(x.rescue_pair_quotes)})
c({x.name: len(x.rescue_quotes) for x in sorted_ if not len(x.rescue_quotes)})
