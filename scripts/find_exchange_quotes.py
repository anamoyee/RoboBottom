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


@dataclass
class AnimalR:
	name: str
	displayname: str
	emoji: str

	def __str__(self):
		return f"ANIMAL_{self.name.upper().replace('-', '').replace(' ', '_')} := AnimalR(name={self.name!r}, displayname={self.displayname!r}, emoji={self.emoji!r})"


ANIMALS = [
	ANIMAL_BACTRIAN_CAMEL := AnimalR(
		name="bactrian camel",
		displayname="Bactrian Camel",
		emoji="🐫",
	),
	ANIMAL_BADGER := AnimalR(
		name="badger",
		displayname="Badger",
		emoji="🦡",
	),
	ANIMAL_BEE := AnimalR(
		name="bee",
		displayname="Bee",
		emoji="🐝",
	),
	ANIMAL_BIRD := AnimalR(
		name="bird",
		displayname="Bird",
		emoji="🐦",
	),
	ANIMAL_BISON := AnimalR(
		name="bison",
		displayname="Bison",
		emoji="🦬",
	),
	ANIMAL_BOAR := AnimalR(
		name="boar",
		displayname="Boar",
		emoji="🐗",
	),
	ANIMAL_BUNNY := AnimalR(
		name="bunny",
		displayname="Bunny",
		emoji="🐇",
	),
	ANIMAL_BUTTERFLY := AnimalR(
		name="butterfly",
		displayname="Butterfly",
		emoji="🦋",
	),
	ANIMAL_CHIPMUNK := AnimalR(
		name="chipmunk",
		displayname="Chipmunk",
		emoji="🐿",
	),
	ANIMAL_COCKROACH := AnimalR(
		name="cockroach",
		displayname="Cockroach",
		emoji="🪳",
	),
	ANIMAL_DODO := AnimalR(
		name="dodo",
		displayname="Dodo",
		emoji="🦤",
	),
	ANIMAL_DOLPHIN := AnimalR(
		name="dolphin",
		displayname="Dolphin",
		emoji="🐬",
	),
	ANIMAL_DONKEY := AnimalR(
		name="donkey",
		displayname="Donkey",
		emoji="🫏",
	),
	ANIMAL_DRAGON := AnimalR(
		name="dragon",
		displayname="Dragon",
		emoji="🐲",
	),
	ANIMAL_EAGLE := AnimalR(
		name="eagle",
		displayname="Eagle",
		emoji="🦅",
	),
	ANIMAL_FLAMINGO := AnimalR(
		name="flamingo",
		displayname="Flamingo",
		emoji="🦩",
	),
	ANIMAL_GOAT := AnimalR(
		name="goat",
		displayname="Goat",
		emoji="🐐",
	),
	ANIMAL_JELLYFISH := AnimalR(
		name="jellyfish",
		displayname="Jellyfish",
		emoji="🪼",
	),
	ANIMAL_KANGAROO := AnimalR(
		name="kangaroo",
		displayname="Kangaroo",
		emoji="🦘",
	),
	ANIMAL_LADYBUG := AnimalR(
		name="ladybug",
		displayname="Ladybug",
		emoji="🐞",
	),
	ANIMAL_LION := AnimalR(
		name="lion",
		displayname="Lion",
		emoji="🦁",
	),
	ANIMAL_LLAMA := AnimalR(
		name="llama",
		displayname="Llama",
		emoji="🦙",
	),
	ANIMAL_LOBSTER := AnimalR(
		name="lobster",
		displayname="Lobster",
		emoji="🦞",
	),
	ANIMAL_MAMMOTH := AnimalR(
		name="mammoth",
		displayname="Mammoth",
		emoji="🦣",
	),
	ANIMAL_MONKEY := AnimalR(
		name="monkey",
		displayname="Monkey",
		emoji="🐒",
	),
	ANIMAL_MOOSE := AnimalR(
		name="moose",
		displayname="Moose",
		emoji="🫎",
	),
	ANIMAL_MOSQUITO := AnimalR(
		name="mosquito",
		displayname="Mosquito",
		emoji="🦟",
	),
	ANIMAL_OCTOPUS := AnimalR(
		name="octopus",
		displayname="Octopus",
		emoji="🐙",
	),
	ANIMAL_ORANGUTAN := AnimalR(
		name="orangutan",
		displayname="Orangutan",
		emoji="🦧",
	),
	ANIMAL_OTTER := AnimalR(
		name="otter",
		displayname="Otter",
		emoji="🦦",
	),
	ANIMAL_OWL := AnimalR(
		name="owl",
		displayname="Owl",
		emoji="🦉",
	),
	ANIMAL_PANDA := AnimalR(
		name="panda",
		displayname="Panda",
		emoji="🐼",
	),
	ANIMAL_PEACOCK := AnimalR(
		name="peacock",
		displayname="Peacock",
		emoji="🦚",
	),
	ANIMAL_POLAR_BEAR := AnimalR(
		name="polar bear",
		displayname="Polar Bear",
		emoji="🐻\u200d❄️",
	),
	ANIMAL_POODLE := AnimalR(
		name="poodle",
		displayname="Poodle",
		emoji="🐩",
	),
	ANIMAL_PUFFERFISH := AnimalR(
		name="pufferfish",
		displayname="Pufferfish",
		emoji="🐡",
	),
	ANIMAL_RACCOON := AnimalR(
		name="raccoon",
		displayname="Raccoon",
		emoji="🦝",
	),
	ANIMAL_RAM := AnimalR(
		name="ram",
		displayname="Ram",
		emoji="🐏",
	),
	ANIMAL_RAT := AnimalR(
		name="rat",
		displayname="Rat",
		emoji="🐀",
	),
	ANIMAL_RHINO := AnimalR(
		name="rhino",
		displayname="Rhino",
		emoji="🦏",
	),
	ANIMAL_ROOSTER := AnimalR(
		name="rooster",
		displayname="Rooster",
		emoji="🐓",
	),
	ANIMAL_SCORPION := AnimalR(
		name="scorpion",
		displayname="Scorpion",
		emoji="🦂",
	),
	ANIMAL_SHARK := AnimalR(
		name="shark",
		displayname="Shark",
		emoji="🦈",
	),
	ANIMAL_SNAKE := AnimalR(
		name="snake",
		displayname="Snake",
		emoji="🐍",
	),
	ANIMAL_SWAN := AnimalR(
		name="swan",
		displayname="Swan",
		emoji="🦢",
	),
	ANIMAL_TREX := AnimalR(
		name="t-rex",
		displayname="T-Rex",
		emoji="🦖",
	),
	ANIMAL_TIGER := AnimalR(
		name="tiger",
		displayname="Tiger",
		emoji="🐯",
	),
	ANIMAL_TURTLE := AnimalR(
		name="turtle",
		displayname="Turtle",
		emoji="🐢",
	),
	ANIMAL_UNICORN := AnimalR(
		name="unicorn",
		displayname="Unicorn",
		emoji="🦄",
	),
	ANIMAL_WOLF := AnimalR(
		name="wolf",
		displayname="Wolf",
		emoji="🐺",
	),
]


c(len(ANIMALS))

export = dcx.Export.from_path(p.Path(__file__).parent / "gitignored/zoo-bot@9tbh.json")


@dataclass
class Processed:
	emoji: str
	an: Literal["an", "a"] | None
	animal: str | None
	quote: str
	orig_first_line: str

	def __post_init__(self):
		self.quote = self.quote.strip()

	def to_animal2(self) -> "AnimalR2":
		_animals1 = [x for x in ANIMALS if x.emoji == self.emoji]

		if len(_animals1) != 1:
			c(_animals1)
			c(self.emoji)
			c(self.orig_first_line)
			raise RuntimeError("len(_animals1) != 1")

		animal1 = _animals1[0]

		return AnimalR2(
			name=animal1.name,
			displayname=animal1.displayname,
			emoji=self.emoji,
			an=self.an == "an",
			exchange_quotes={self.quote},
		)


@dataclass
class AnimalR2(AnimalR):
	an: bool
	exchange_quotes: set[str]

	def __str__(self):
		return f"ANIMAL_{self.name.upper().replace('-', '').replace(' ', '_')} := AnimalR(name={self.name!r}, displayname={self.displayname!r}, emoji={self.emoji!r}, an={self.an!r}, exchange_quotes={repr(self.exchange_quotes)[:-1] + ',}'},)"

	def merge(self, other: "AnimalR2") -> "AnimalR2":
		return AnimalR2(
			name=self.name,
			displayname=self.displayname,
			emoji=self.emoji,
			an=self.an,
			exchange_quotes=self.exchange_quotes | other.exchange_quotes,
		)

	@classmethod
	def merge_all(cls: type["AnimalR2"], animals: list["AnimalR2"]) -> list["AnimalR2"]:
		"""Merge all animals with the same emoji."""
		grouped_animals: dict[str, list[AnimalR2]] = defaultdict(list)

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

	if not message.content.startswith("✨"):
		continue

	first_line = message.content.split("\n")[0]

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

	if "You have been freed of your curse" in first_line:
		continue

	if " now has " in first_line:  # '/set' i think?
		continue

	if is_april_fools_range(message.timestamp):  # skip pokemon stuff throwing off the search
		continue

	# first_line = re.sub(r"(you have \d+)$", "", first_line)
	PATT = re.compile(r"^✨ You exchanged for (?P<an>a|an|\d+) (?P<emoji>.)[^ ]* \*\*(?P<animal>\D+?)\*\*! ?(?P<quote>.*)?$", re.RegexFlag.I | re.RegexFlag.U)

	t0 = time.perf_counter()

	m = PATT.match(first_line)

	t1 = time.perf_counter()
	elapsed = datetime.datetime.fromtimestamp(t1, tz=datetime.UTC) - datetime.datetime.fromtimestamp(t0, tz=datetime.UTC)

	if not m:
		c.warn("huh?: " + repr(first_line))
		continue

	if m.group("an").isdigit():
		continue

	if m.group("emoji") in ("🦌", "☃", "🐠"):
		continue

	dct = m.groupdict()

	if m.group("emoji") == "🐻":
		dct["emoji"] = "🐻\u200d❄️"

	processedes.append(Processed(**dct, orig_first_line=first_line))

c(len(processedes))

generated = [x.to_animal2() for x in processedes]

merged = AnimalR2.merge_all(generated)

sorted_ = sorted(merged, key=lambda x: x.name)

for animal2 in sorted_:
	print(animal2, end=",\n")

c(len(sorted_))
