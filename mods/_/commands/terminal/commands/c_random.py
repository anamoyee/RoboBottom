import random as rng
import string
from dataclasses import dataclass, field

from .._base import *
from .._base import TerminalCommand as Cmd

if True:  # Piglin Stuff

	@dataclass
	class PiglinDrop:
		name: str = field(kw_only=False)
		amount_tup: tuple[int, int] = field(kw_only=True)  # Represents level sometimes
		weight: int = field(kw_only=True)

		def __str__(self) -> str:
			amount = rng.randint(*self.amount_tup)
			chance = float(self.weight / PIGLIN_WEIGHTS_SUM)

			return f"{
				self.name.replace(f'{{amount}}', str(amount)).replace(f'{{level}}', ''.join(['I'] * amount))  # Never goes beyond III so it's fine
			} ({chance * 100:.2f}%)"

	PIGLIN_DROPS = [ # Source: https://minecraft.wiki/w/Bartering
		PiglinDrop("Soul Speed {level} Enchanted Book", amount_tup=(1, 3),   weight=5),
		PiglinDrop("Soul Speed {level} Iron Boots",     amount_tup=(1, 3),   weight=8),
		PiglinDrop("Splash Potion of Fire Resistance",  amount_tup=(1, 1),   weight=8),
		PiglinDrop("Potion of Fire Resistance",         amount_tup=(1, 1),   weight=8),
		PiglinDrop("Water Bottle",                      amount_tup=(1, 1),   weight=10),
		PiglinDrop("Iron Nugget ⨯{amount}",             amount_tup=(10, 36), weight=10),  # noqa: RUF001
		PiglinDrop("Ender Pearl ⨯{amount}",             amount_tup=(2, 4),   weight=10),  # noqa: RUF001
		PiglinDrop("String ⨯{amount}",                  amount_tup=(3, 9),   weight=20),  # noqa: RUF001
		PiglinDrop("Nether Quartz ⨯{amount}",           amount_tup=(5, 12),  weight=20),  # noqa: RUF001
		PiglinDrop("Obsidian ⨯{amount}",                amount_tup=(1, 1),   weight=40),  # noqa: RUF001
		PiglinDrop("Crying Obsidian ⨯{amount}",         amount_tup=(1, 3),   weight=40),  # noqa: RUF001
		PiglinDrop("Fire Charge ⨯{amount}",             amount_tup=(1, 1),   weight=40),  # noqa: RUF001
		PiglinDrop("Leather ⨯{amount}",                 amount_tup=(2, 4),   weight=40),  # noqa: RUF001
		PiglinDrop("Soul Sand ⨯{amount}",               amount_tup=(2, 8),   weight=40),  # noqa: RUF001
		PiglinDrop("Nether Brick ⨯{amount}",            amount_tup=(2, 8),   weight=40),  # noqa: RUF001
		PiglinDrop("Spectral Arrow ⨯{amount}",          amount_tup=(6, 12),  weight=40),  # noqa: RUF001
		PiglinDrop("Gravel ⨯{amount}",                  amount_tup=(8, 16),  weight=40),  # noqa: RUF001
		PiglinDrop("Blackstone ⨯{amount}",              amount_tup=(8, 16),  weight=40),  # noqa: RUF001
	]  # fmt: skip
	PIGLIN_WEIGHTS_SUM = sum(piglin_drop.weight for piglin_drop in PIGLIN_DROPS)

	def get_random_piglin_drop() -> PiglinDrop:
		return rng.choices(PIGLIN_DROPS, weights=[piglin_drop.weight for piglin_drop in PIGLIN_DROPS], k=1)[0]


if True:  # Animal Stuff
	ANIMALS = {
		"bat": "🦇",
		"bear": "🐻",
		"beaver": "🦫",
		"beetle": "🪲",
		"caterpillar": "🐛",
		"cat": "🐱",
		"chicken": "🐔",
		"cow": "🐄",
		"crab": "🦀",
		"cricket": "🦗",
		"crocodile": "🐊",
		"dog": "🐶",
		"dove": "🕊️",
		"camel": "🐪",
		"duck": "🦆",
		"elephant": "🐘",
		"fish": "🐟",
		"fly": "🪰",
		"fox": "🦊",
		"frog": "🐸",
		"giraffe": "🦒",
		"gorilla": "🦍",
		"hamster": "🐹",
		"chick": "🐥",
		"hedgehog": "🦔",
		"hippo": "🦛",
		"horse": "🐴",
		"koala": "🐨",
		"leopard": "🐆",
		"lizard": "🦎",
		"mouse": "🐭",
		"ox": "🐂",
		"parrot": "🦜",
		"penguin": "🐧",
		"pig": "🐷",
		"rabbit": "🐰",
		"dinosaur": "🦕",
		"seal": "🦭",
		"sheep": "🐑",
		"shrimp": "🦐",
		"skunk": "🦨",
		"sloth": "🦥",
		"snail": "🐌",
		"snowman": "⛄",
		"spider": "🕷️",
		"squid": "🦑",
		"turkey": "🦃",
		"whale": "🐳",
		"worm": "🪱",
		"zebra": "🦓",
	}

	def get_random_animal_str() -> str:
		key = rng.choice(list(ANIMALS.keys()))
		value = ANIMALS[key]

		return f"{value} {key.title()}"


async def _random(*args: str, **_) -> hikari.Embed:
	coin = rng.choice(["Tails", "Heads"])  # Tails my beloved :3 >w< (the sonic character, not the coin outcome, duh)
	rps = rng.choice(["Rock", "Paper", "Scissors"])
	dice = rng.choice(["1 ⚀", "2 ⚁", "3 ⚂", "4 ⚃", "5 ⚄", "6 ⚅"])
	card_rank = rng.choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])
	card_suit = rng.choice(["♠", "♡", "♢", "♣"])
	color = rng.randint(0x000000, 0xFFFFFF)
	letters = "".join(rng.choices(string.ascii_letters, k=rng.randint(5, 10)))
	month = rng.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
	weekday = rng.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
	piglin = get_random_piglin_drop().__str__()
	animal = get_random_animal_str()

	description_dict = {
		"Coin": coin,
		"RPS": rps,
		"Dice": dice,
		"Card": f"{card_rank} {card_suit}",
		"Color": hex(color).replace("0x", "#"),
		"Letters": letters,
		"Month": month,
		"Weekday": weekday,
		"Piglin": piglin,
		"Animal": animal,
	}

	if args:
		argument = rng.choice(args)
		description_dict["Argument"] = argument

	description = "\n".join(f"**{k}**: {v}" for k, v in description_dict.items() if k is not None)

	description += f"\n\
**{rng.randint(1, int(1e1))}**/{int(1e1)} | \
**{rng.randint(1, int(1e2))}**/{int(1e2)} | \
**{rng.randint(1, int(1e3))}**/{int(1e3)} | \
**{rng.randint(1, int(1e6))}**/{int(1e6)}"

	return hikari.Embed(
		title=None,
		description=description,
		color=color,
	)


random = Cmd(
	callback=_random,
	displayname="random",
	description="Generates every random thing you could possibly ask for",
	usage=["random [args?]"],
	aliases=["rng"],
)
