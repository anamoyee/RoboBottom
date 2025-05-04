true = True
false = False
null = None
from dataclasses import dataclass

from tcrutils.console import c


@dataclass
class A:
	name: str
	amount: int
	emoji: str
	emojiName: str
	family: str
	rare: bool
	pinned: bool


@dataclass
class A2:
	name: str
	displayname: str
	emoji: str
	rare: bool

	def __str__(self):
		return f"ANIMAL_{self.name.upper().replace('-', '').replace(' ', '_')} := Animal(name={self.name!r}, displayname={self.displayname!r}, emoji={self.emoji!r}, rare={self.rare!r},)"


s1 = [
	{"name": "Bat", "amount": 14, "emoji": "🦇", "emojiName": "bat", "family": "bat", "rare": false, "pinned": null},
	{"name": "Owl", "amount": 4, "emoji": "🦉", "emojiName": "owl", "family": "bat", "rare": true, "pinned": null},
	{"name": "Bear", "amount": 12, "emoji": "🐻", "emojiName": "bear", "family": "bear", "rare": false, "pinned": null},
	{"name": "Panda", "amount": 2, "emoji": "🐼", "emojiName": "panda", "family": "bear", "rare": true, "pinned": null},
	{"name": "Beaver", "amount": 28, "emoji": "🦫", "emojiName": "beaver", "family": "beaver", "rare": false, "pinned": null},
	{"name": "Otter", "amount": 2, "emoji": "🦦", "emojiName": "otter", "family": "beaver", "rare": true, "pinned": null},
	{"name": "Beetle", "amount": 39, "emoji": "🪲", "emojiName": "beetle", "family": "beetle", "rare": false, "pinned": null},
	{"name": "Ladybug", "amount": 2, "emoji": "🐞", "emojiName": "ladybug", "family": "beetle", "rare": true, "pinned": null},
	{"name": "Camel", "amount": 9, "emoji": "🐪", "emojiName": "camel", "family": "camel", "rare": false, "pinned": null},
	{"name": "Bactrian Camel", "amount": 4, "emoji": "🐫", "emojiName": "bactrian_camel", "family": "camel", "rare": true, "pinned": null},
	{"name": "Cat", "amount": 0, "emoji": "🐱", "emojiName": "cat", "family": "cat", "rare": false, "pinned": null},
	{"name": "Tiger", "amount": 1, "emoji": "🐯", "emojiName": "tiger", "family": "cat", "rare": true, "pinned": null},
	{"name": "Caterpillar", "amount": 9, "emoji": "🐛", "emojiName": "caterpillar", "family": "caterpillar", "rare": false, "pinned": null},
	{"name": "Butterfly", "amount": 2, "emoji": "🦋", "emojiName": "butterfly", "family": "caterpillar", "rare": true, "pinned": null},
	{"name": "Chick", "amount": 34, "emoji": "🐥", "emojiName": "chick", "family": "chick", "rare": false, "pinned": null},
	{"name": "Bird", "amount": 2, "emoji": "🐦", "emojiName": "bird", "family": "chick", "rare": true, "pinned": null},
	{"name": "Chicken", "amount": 7, "emoji": "🐔", "emojiName": "chicken", "family": "chicken", "rare": false, "pinned": null},
	{"name": "Rooster", "amount": 5, "emoji": "🐓", "emojiName": "rooster", "family": "chicken", "rare": true, "pinned": null},
	{"name": "Cow", "amount": 9, "emoji": "🐄", "emojiName": "cow", "family": "cow", "rare": false, "pinned": null},
	{"name": "Goat", "amount": 2, "emoji": "🐐", "emojiName": "goat", "family": "cow", "rare": true, "pinned": null},
	{"name": "Crab", "amount": 33, "emoji": "🦀", "emojiName": "crab", "family": "crab", "rare": false, "pinned": null},
	{"name": "Lobster", "amount": 2, "emoji": "🦞", "emojiName": "lobster", "family": "crab", "rare": true, "pinned": null},
	{"name": "Cricket", "amount": 29, "emoji": "🦗", "emojiName": "cricket", "family": "cricket", "rare": false, "pinned": null},
	{"name": "Cockroach", "amount": 2, "emoji": "🪳", "emojiName": "cockroach", "family": "cricket", "rare": true, "pinned": null},
	{"name": "Crocodile", "amount": 29, "emoji": "🐊", "emojiName": "crocodile", "family": "crocodile", "rare": false, "pinned": null},
	{"name": "Pufferfish", "amount": 2, "emoji": "🐡", "emojiName": "pufferfish", "family": "crocodile", "rare": true, "pinned": null},
	{"name": "Deer", "amount": 31, "emoji": "🦌", "emojiName": "deer", "family": "deer", "rare": false, "pinned": null},
	{"name": "Moose", "amount": 2, "emoji": "🫎", "emojiName": "moose", "family": "deer", "rare": true, "pinned": null},
	{"name": "Dinosaur", "amount": 9, "emoji": "🦕", "emojiName": "dinosaur", "family": "dinosaur", "rare": false, "pinned": null},
	{"name": "T-Rex", "amount": 1, "emoji": "🦖", "emojiName": "t_rex", "family": "dinosaur", "rare": true, "pinned": null},
	{"name": "Dog", "amount": 22, "emoji": "🐶", "emojiName": "dog", "family": "dog", "rare": false, "pinned": null},
	{"name": "Poodle", "amount": 2, "emoji": "🐩", "emojiName": "poodle", "family": "dog", "rare": true, "pinned": null},
	{"name": "Dove", "amount": 30, "emoji": "🕊️", "emojiName": "dove", "family": "dove", "rare": false, "pinned": null},
	{"name": "Eagle", "amount": 2, "emoji": "🦅", "emojiName": "eagle", "family": "dove", "rare": true, "pinned": null},
	{"name": "Duck", "amount": 35, "emoji": "🦆", "emojiName": "duck", "family": "duck", "rare": false, "pinned": null},
	{"name": "Swan", "amount": 2, "emoji": "🦢", "emojiName": "swan", "family": "duck", "rare": true, "pinned": null},
	{"name": "Elephant", "amount": 22, "emoji": "🐘", "emojiName": "elephant", "family": "elephant", "rare": false, "pinned": null},
	{"name": "Mammoth", "amount": 2, "emoji": "🦣", "emojiName": "mammoth", "family": "elephant", "rare": true, "pinned": null},
	{"name": "Fish", "amount": 37, "emoji": "🐟", "emojiName": "fish", "family": "fish", "rare": false, "pinned": null},
	{"name": "Jellyfish", "amount": 2, "emoji": "🪼", "emojiName": "jellyfish", "family": "fish", "rare": true, "pinned": null},
	{"name": "Fly", "amount": 11, "emoji": "🪰", "emojiName": "fly", "family": "fly", "rare": false, "pinned": null},
	{"name": "Mosquito", "amount": 2, "emoji": "🦟", "emojiName": "mosquito", "family": "fly", "rare": true, "pinned": null},
	{"name": "Fox", "amount": 475, "emoji": "🦊", "emojiName": "fox", "family": "fox", "rare": false, "pinned": "red"},
	{"name": "Wolf", "amount": 3, "emoji": "🐺", "emojiName": "wolf", "family": "fox", "rare": true, "pinned": null},
	{"name": "Frog", "amount": 37, "emoji": "🐸", "emojiName": "frog", "family": "frog", "rare": false, "pinned": null},
	{"name": "Turtle", "amount": 2, "emoji": "🐢", "emojiName": "turtle", "family": "frog", "rare": true, "pinned": null},
	{"name": "Giraffe", "amount": 37, "emoji": "🦒", "emojiName": "giraffe", "family": "giraffe", "rare": false, "pinned": null},
	{"name": "Kangaroo", "amount": 2, "emoji": "🦘", "emojiName": "kangaroo", "family": "giraffe", "rare": true, "pinned": null},
	{"name": "Gorilla", "amount": 21, "emoji": "🦍", "emojiName": "gorilla", "family": "gorilla", "rare": false, "pinned": null},
	{"name": "Orangutan", "amount": 2, "emoji": "🦧", "emojiName": "orangutan", "family": "gorilla", "rare": true, "pinned": null},
	{"name": "Hamster", "amount": 25, "emoji": "🐹", "emojiName": "hamster", "family": "hamster", "rare": false, "pinned": null},
	{"name": "Chipmunk", "amount": 2, "emoji": "🐿️", "emojiName": "chipmunk", "family": "hamster", "rare": true, "pinned": null},
	{"name": "Hedgehog", "amount": 26, "emoji": "🦔", "emojiName": "hedgehog", "family": "hedgehog", "rare": false, "pinned": null},
	{"name": "Donkey", "amount": 2, "emoji": "🫏", "emojiName": "donkey", "family": "hedgehog", "rare": true, "pinned": null},
	{"name": "Hippo", "amount": 29, "emoji": "🦛", "emojiName": "hippo", "family": "hippo", "rare": false, "pinned": null},
	{"name": "Rhino", "amount": 2, "emoji": "🦏", "emojiName": "rhino", "family": "hippo", "rare": true, "pinned": null},
	{"name": "Horse", "amount": 27, "emoji": "🐴", "emojiName": "horse", "family": "horse", "rare": false, "pinned": null},
	{"name": "Unicorn", "amount": 3, "emoji": "🦄", "emojiName": "unicorn", "family": "horse", "rare": true, "pinned": null},
	{"name": "Koala", "amount": 42, "emoji": "🐨", "emojiName": "koala", "family": "koala", "rare": false, "pinned": null},
	{"name": "Raccoon", "amount": 1, "emoji": "🦝", "emojiName": "raccoon", "family": "koala", "rare": true, "pinned": null},
	{"name": "Leopard", "amount": 33, "emoji": "🐆", "emojiName": "leopard", "family": "leopard", "rare": false, "pinned": null},
	{"name": "Lion", "amount": 2, "emoji": "🦁", "emojiName": "lion", "family": "leopard", "rare": true, "pinned": null},
	{"name": "Lizard", "amount": 34, "emoji": "🦎", "emojiName": "lizard", "family": "lizard", "rare": false, "pinned": null},
	{"name": "Dragon", "amount": 3, "emoji": "🐲", "emojiName": "dragon", "family": "lizard", "rare": true, "pinned": null},
	{"name": "Mouse", "amount": 29, "emoji": "🐭", "emojiName": "mouse", "family": "mouse", "rare": false, "pinned": null},
	{"name": "Rat", "amount": 2, "emoji": "🐀", "emojiName": "rat", "family": "mouse", "rare": true, "pinned": null},
	{"name": "Ox", "amount": 24, "emoji": "🐂", "emojiName": "ox", "family": "ox", "rare": false, "pinned": null},
	{"name": "Bison", "amount": 2, "emoji": "🦬", "emojiName": "bison", "family": "ox", "rare": true, "pinned": null},
	{"name": "Parrot", "amount": 35, "emoji": "🦜", "emojiName": "parrot", "family": "parrot", "rare": false, "pinned": null},
	{"name": "Peacock", "amount": 2, "emoji": "🦚", "emojiName": "peacock", "family": "parrot", "rare": true, "pinned": null},
	{"name": "Penguin", "amount": 35, "emoji": "🐧", "emojiName": "penguin", "family": "penguin", "rare": false, "pinned": null},
	{"name": "Polar Bear", "amount": 2, "emoji": "🐻‍❄️", "emojiName": "polar_bear", "family": "penguin", "rare": true, "pinned": null},
	{"name": "Pig", "amount": 37, "emoji": "🐷", "emojiName": "pig", "family": "pig", "rare": false, "pinned": null},
	{"name": "Boar", "amount": 2, "emoji": "🐗", "emojiName": "boar", "family": "pig", "rare": true, "pinned": null},
	{"name": "Rabbit", "amount": 10, "emoji": "🐰", "emojiName": "rabbit", "family": "rabbit", "rare": false, "pinned": null},
	{"name": "Bunny", "amount": 2, "emoji": "🐇", "emojiName": "bunny", "family": "rabbit", "rare": true, "pinned": null},
	{"name": "Seal", "amount": 23, "emoji": "🦭", "emojiName": "seal", "family": "seal", "rare": false, "pinned": null},
	{"name": "Dolphin", "amount": 2, "emoji": "🐬", "emojiName": "dolphin", "family": "seal", "rare": true, "pinned": null},
	{"name": "Sheep", "amount": 25, "emoji": "🐑", "emojiName": "sheep", "family": "sheep", "rare": false, "pinned": null},
	{"name": "Ram", "amount": 2, "emoji": "🐏", "emojiName": "ram", "family": "sheep", "rare": true, "pinned": null},
	{"name": "Shrimp", "amount": 26, "emoji": "🦐", "emojiName": "shrimp", "family": "shrimp", "rare": false, "pinned": null},
	{"name": "Flamingo", "amount": 2, "emoji": "🦩", "emojiName": "flamingo", "family": "shrimp", "rare": true, "pinned": null},
	{"name": "Skunk", "amount": 32, "emoji": "🦨", "emojiName": "skunk", "family": "skunk", "rare": false, "pinned": null},
	{"name": "Badger", "amount": 2, "emoji": "🦡", "emojiName": "badger", "family": "skunk", "rare": true, "pinned": null},
	{"name": "Sloth", "amount": 21, "emoji": "🦥", "emojiName": "sloth", "family": "sloth", "rare": false, "pinned": null},
	{"name": "Monkey", "amount": 2, "emoji": "🐒", "emojiName": "monkey", "family": "sloth", "rare": true, "pinned": null},
	{"name": "Snail", "amount": 9, "emoji": "🐌", "emojiName": "snail", "family": "snail", "rare": false, "pinned": null},
	{"name": "Bee", "amount": 5, "emoji": "🐝", "emojiName": "bee", "family": "snail", "rare": true, "pinned": null},
	{"name": "Spider", "amount": 34, "emoji": "🕷️", "emojiName": "spider", "family": "spider", "rare": false, "pinned": null},
	{"name": "Scorpion", "amount": 2, "emoji": "🦂", "emojiName": "scorpion", "family": "spider", "rare": true, "pinned": null},
	{"name": "Squid", "amount": 32, "emoji": "🦑", "emojiName": "squid", "family": "squid", "rare": false, "pinned": null},
	{"name": "Octopus", "amount": 2, "emoji": "🐙", "emojiName": "octopus", "family": "squid", "rare": true, "pinned": null},
	{"name": "Turkey", "amount": 36, "emoji": "🦃", "emojiName": "turkey", "family": "turkey", "rare": false, "pinned": null},
	{"name": "Dodo", "amount": 2, "emoji": "🦤", "emojiName": "dodo", "family": "turkey", "rare": true, "pinned": null},
	{"name": "Whale", "amount": 33, "emoji": "🐳", "emojiName": "whale", "family": "whale", "rare": false, "pinned": null},
	{"name": "Shark", "amount": 2, "emoji": "🦈", "emojiName": "shark", "family": "whale", "rare": true, "pinned": null},
	{"name": "Worm", "amount": 34, "emoji": "🪱", "emojiName": "worm", "family": "worm", "rare": false, "pinned": null},
	{"name": "Snake", "amount": 5, "emoji": "🐍", "emojiName": "snake", "family": "worm", "rare": true, "pinned": null},
	{"name": "Zebra", "amount": 13, "emoji": "🦓", "emojiName": "zebra", "family": "zebra", "rare": false, "pinned": null},
	{"name": "Llama", "amount": 2, "emoji": "🦙", "emojiName": "llama", "family": "zebra", "rare": true, "pinned": null},
]

s2 = [A(**d) for d in s1]

m_c = """
ANIMAL_FOX := Animal(
		name="fox",
		displayname="Fox",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_KOALA := Animal(
		name="koala",
		displayname="Koala",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_BEETLE := Animal(
		name="beetle",
		displayname="Beetle",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_GIRAFFE := Animal(
		name="giraffe",
		displayname="Giraffe",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_FROG := Animal(
		name="frog",
		displayname="Frog",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_FISH := Animal(
		name="fish",
		displayname="Fish",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_PIG := Animal(
		name="pig",
		displayname="Pig",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_TURKEY := Animal(
		name="turkey",
		displayname="Turkey",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_PARROT := Animal(
		name="parrot",
		displayname="Parrot",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_DUCK := Animal(
		name="duck",
		displayname="Duck",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_PENGUIN := Animal(
		name="penguin",
		displayname="Penguin",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CHICK := Animal(
		name="chick",
		displayname="Chick",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_LIZARD := Animal(
		name="lizard",
		displayname="Lizard",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_WORM := Animal(
		name="worm",
		displayname="Worm",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SPIDER := Animal(
		name="spider",
		displayname="Spider",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_LEOPARD := Animal(
		name="leopard",
		displayname="Leopard",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CRAB := Animal(
		name="crab",
		displayname="Crab",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_WHALE := Animal(
		name="whale",
		displayname="Whale",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SQUID := Animal(
		name="squid",
		displayname="Squid",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SKUNK := Animal(
		name="skunk",
		displayname="Skunk",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_DEER := Animal(
		name="deer",
		displayname="Deer",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_DOVE := Animal(
		name="dove",
		displayname="Dove",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CRICKET := Animal(
		name="cricket",
		displayname="Cricket",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_HIPPO := Animal(
		name="hippo",
		displayname="Hippo",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CROCODILE := Animal(
		name="crocodile",
		displayname="Crocodile",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_MOUSE := Animal(
		name="mouse",
		displayname="Mouse",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_BEAVER := Animal(
		name="beaver",
		displayname="Beaver",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_HORSE := Animal(
		name="horse",
		displayname="Horse",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SHRIMP := Animal(
		name="shrimp",
		displayname="Shrimp",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_HEDGEHOG := Animal(
		name="hedgehog",
		displayname="Hedgehog",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SHEEP := Animal(
		name="sheep",
		displayname="Sheep",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_HAMSTER := Animal(
		name="hamster",
		displayname="Hamster",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_OX := Animal(
		name="ox",
		displayname="Ox",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SEAL := Animal(
		name="seal",
		displayname="Seal",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_DOG := Animal(
		name="dog",
		displayname="Dog",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SLOTH := Animal(
		name="sloth",
		displayname="Sloth",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_ELEPHANT := Animal(
		name="elephant",
		displayname="Elephant",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_GORILLA := Animal(
		name="gorilla",
		displayname="Gorilla",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_BAT := Animal(
		name="bat",
		displayname="Bat",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_ZEBRA := Animal(
		name="zebra",
		displayname="Zebra",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_BEAR := Animal(
		name="bear",
		displayname="Bear",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_FLY := Animal(
		name="fly",
		displayname="Fly",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_RABBIT := Animal(
		name="rabbit",
		displayname="Rabbit",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CATERPILLAR := Animal(
		name="caterpillar",
		displayname="Caterpillar",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_SNAIL := Animal(
		name="snail",
		displayname="Snail",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_DINOSAUR := Animal(
		name="dinosaur",
		displayname="Dinosaur",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CAMEL := Animal(
		name="camel",
		displayname="Camel",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_COW := Animal(
		name="cow",
		displayname="Cow",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CHICKEN := Animal(
		name="chicken",
		displayname="Chicken",
		emoji="🦊",
		rare=False,
	),
	ANIMAL_CAT := Animal(
		name="cat",
		displayname="Cat",
		emoji="🦊",
		rare=False,
	),
"""


m_r = """

	ANIMAL_WOLF := Animal(
		name="wolf",
		displayname="Wolf",
		emoji="🐺",
		rare=True,
	),
	ANIMAL_ROOSTER := Animal(
		name="rooster",
		displayname="Rooster",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BEE := Animal(
		name="bee",
		displayname="Bee",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_SNAKE := Animal(
		name="snake",
		displayname="Snake",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_OWL := Animal(
		name="owl",
		displayname="Owl",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BACTRIAN_CAMEL := Animal(
		name="bactrian camel",
		displayname="Bactrian Camel",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_UNICORN := Animal(
		name="unicorn",
		displayname="Unicorn",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_DRAGON := Animal(
		name="dragon",
		displayname="Dragon",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_RAM := Animal(
		name="ram",
		displayname="Ram",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_POODLE := Animal(
		name="poodle",
		displayname="Poodle",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_CHIPMUNK := Animal(
		name="chipmunk",
		displayname="Chipmunk",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_KANGAROO := Animal(
		name="kangaroo",
		displayname="Kangaroo",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_LLAMA := Animal(
		name="llama",
		displayname="Llama",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_DODO := Animal(
		name="dodo",
		displayname="Dodo",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_MONKEY := Animal(
		name="monkey",
		displayname="Monkey",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BIRD := Animal(
		name="bird",
		displayname="Bird",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_EAGLE := Animal(
		name="eagle",
		displayname="Eagle",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_LION := Animal(
		name="lion",
		displayname="Lion",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BUTTERFLY := Animal(
		name="butterfly",
		displayname="Butterfly",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_COCKROACH := Animal(
		name="cockroach",
		displayname="Cockroach",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_LADYBUG := Animal(
		name="ladybug",
		displayname="Ladybug",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_TURTLE := Animal(
		name="turtle",
		displayname="Turtle",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_PEACOCK := Animal(
		name="peacock",
		displayname="Peacock",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_MOSQUITO := Animal(
		name="mosquito",
		displayname="Mosquito",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_JELLYFISH := Animal(
		name="jellyfish",
		displayname="Jellyfish",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_SWAN := Animal(
		name="swan",
		displayname="Swan",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_OTTER := Animal(
		name="otter",
		displayname="Otter",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_LOBSTER := Animal(
		name="lobster",
		displayname="Lobster",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_FLAMINGO := Animal(
		name="flamingo",
		displayname="Flamingo",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_OCTOPUS := Animal(
		name="octopus",
		displayname="Octopus",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_SHARK := Animal(
		name="shark",
		displayname="Shark",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_RHINO := Animal(
		name="rhino",
		displayname="Rhino",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_PUFFERFISH := Animal(
		name="pufferfish",
		displayname="Pufferfish",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_DOLPHIN := Animal(
		name="dolphin",
		displayname="Dolphin",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_RAT := Animal(
		name="rat",
		displayname="Rat",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_SCORPION := Animal(
		name="scorpion",
		displayname="Scorpion",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BADGER := Animal(
		name="badger",
		displayname="Badger",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_MOOSE := Animal(
		name="moose",
		displayname="Moose",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_POLAR_BEAR := Animal(
		name="polar bear",
		displayname="Polar Bear",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_DONKEY := Animal(
		name="donkey",
		displayname="Donkey",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BUNNY := Animal(
		name="bunny",
		displayname="Bunny",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_MAMMOTH := Animal(
		name="mammoth",
		displayname="Mammoth",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_ORANGUTAN := Animal(
		name="orangutan",
		displayname="Orangutan",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BOAR := Animal(
		name="boar",
		displayname="Boar",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_BISON := Animal(
		name="bison",
		displayname="Bison",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_PANDA := Animal(
		name="panda",
		displayname="Panda",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_GOAT := Animal(
		name="goat",
		displayname="Goat",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_RACCOON := Animal(
		name="raccoon",
		displayname="Raccoon",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_TREX := Animal(
		name="t-rex",
		displayname="T-Rex",
		emoji="🦊",
		rare=True,
	),
	ANIMAL_TIGER := Animal(
		name="tiger",
		displayname="Tiger",
		emoji="🦊",
		rare=True,
	),
"""


def convert(s: str) -> list[A2]:
	return [A2(**{y.strip().split("=")[0].strip(): eval(y.strip().split("=")[1].strip()) for y in x.strip().split(":=")[1].strip().removeprefix("Animal")[1:].strip(",").split(",")}) for x in s.strip().strip("),").split("),")]


m_c2 = convert(m_c)
m_r2 = convert(m_r)


def convert2(l: list[A2]) -> None:
	for a2 in l:
		a = [a for a in s2 if a.name == a2.displayname]

		assert len(a) == 1

		a: A = a[0]

		a2.emoji = a.emoji


convert2(m_c2)
convert2(m_r2)


def sort(l: list[A2]):
	l.sort(key=lambda x: x.name)


sort(m_c2)
sort(m_r2)


def convert3(l: list[A2]) -> str:
	return ",\n".join(str(a2) for a2 in l) + ","


print(convert3(m_c2))
print("-----------------")
print(convert3(m_r2))
