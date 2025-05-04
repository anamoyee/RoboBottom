from prelude import get_logger

from ._base import *

if True:  # statics
	BASE_RESCUE_VERBS = {
		"found",
		"came across",
		"hatched",
		"caught",
		"restored",
		"charmed",
		"adopted",
		"ran into",
		"rung up",
		"scooped up",
		"brought forth",
		"captivated",
		"attracted",
		"joined forces with",
		"invoked",
		"called upon",
		"insured",
		"summoned",
		"baited",
		"screenshotted",
		"picked up",
		"crossed paths with",
		"brought home",
		"rescued",
		"excited",
		"bred",
		"encountered",
		"discovered",
		"befriended",
		"recruited",
	}
	"""Verbs not specific to any animal, when getting a random verb, get any from either this pool or the animal's .rescue_verbs pool."""


if True:  # types

	class Animal(HasEmoji):
		"""Ownerless animal representation, if owned, will be included as a mapping of animals: `dict[Animal.name: str, amount: int]`."""

		name: str
		"""The (internal, not display) name of this animal."""

		displayname: str
		"""The displayname of this animal."""

		an: str
		"""Whether or not the animal should be referred to as `an {displayname}` or `a {displayname}`."""

		def str_listitem(self, *, count: int | None = None, pinned: bool | None = None, loopback_link_ctx: arc.GatewayContext | None = None) -> str:
			if loopback_link_ctx is None:
				displayname = self.displayname
			else:
				displayname = self.displayname if not self.rare else make_loopback_channel_link(loopback_link_ctx, self.displayname, tip="Rare version of TODO")  # TODO: how to fetch the common animal's name

			s = f"{self.emoji} **{displayname}**"

			if count is not None:
				s += f" ⨯{count}"  # noqa: RUF001

			if pinned:
				s += " 📌"

			return s

		@property
		def rare(self) -> bool:
			return isinstance(self, AnimalR)

		@classmethod
		def from_name(cls, name: str):
			return ANIMALS[name]

	class AnimalC(Animal):
		"""Ownerless common animal representation, if owned, will be included as a mapping of animals: `dict[AnimalC.name: str, amount: int]`."""

		rescue_verbs: set[str]
		"""Additional verbs (from base verbs for all animals) to the pool of verbs for this animal when rescuing it via /rescue"""

		rescue_quotes: set[str]
		"""A set of quotes shown upon rescuing this animal via /rescue"""

		rescue_pair_quotes: set[str]
		"""A set of quotes shown upon rescuing this animal in a pair via /rescue"""

		def get_random_rescue_verb(self) -> str:
			return random.choice((*self.rescue_verbs, *BASE_RESCUE_VERBS))

		def get_random_rescue_quote(self, *, is_pair: bool) -> str:
			if is_pair:
				if not self.rescue_pair_quotes:
					return ""

				return random.choice((*self.rescue_pair_quotes,))
			else:
				if not self.rescue_quotes:
					return ""

				return random.choice((*self.rescue_quotes,))

		@classmethod
		def from_name(cls, name: str):
			return COMMON_ANIMALS[name]

	class AnimalR(Animal):
		"""Ownerless rare animal representation, if owned, will be included as a mapping of animals: `dict[AnimalR.name: str, amount: int]`."""

		exchange_quotes: set[str]
		"""A set of quotes shown upon exchanging to this animal via /exchange"""

		@classmethod
		def from_name(cls, name: str):
			return RARE_ANIMALS[name]


if True:  # instances
	COMMON_ANIMALS: dict[str, AnimalC] = {
		animal.name: animal
		for animal in (
			AnimalC(
				name="bat",
				displayname="Bat",
				emoji="🦇",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He seems to care a lot about justice.",
					"Sounds delicious!",
					"She's trying to get off the menu.",
					"He demands blood and potatoes.",
					"The doom of humanity.",
					"She seems to care a lot about justice.",
				},
				rescue_pair_quotes={
					"Zoinks!",
				},
			),
			AnimalC(
				name="bear",
				displayname="Bear",
				emoji="🐻",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"They have stripes because it's better than being spotted.",
					"She chirps with excitement.",
					"Remain calm and stand tall.",
					"She slowly approaches.",
					"He slowly approaches.",
					"Where are you even going to put him?",
					"We did it, boys.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Nice going!",
					"Or maybe one is an echidna.",
					"Sweet!",
				},
			),
			AnimalC(
				name="beaver",
				displayname="Beaver",
				emoji="🦫",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Apparently they have a personal vendetta against flowing water.",
					"Oh man!",
					"Don't expect your wood to last.",
				},
				rescue_pair_quotes={
					"Nice going!",
					"Well I'll be dammed!",
				},
			),
			AnimalC(
				name="beetle",
				displayname="Beetle",
				emoji="🪲",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Better submit a bug report.",
					"He performs rock music sometimes.",
					"She performs rock music sometimes.",
					"We did it, boys.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="camel",
				displayname="Camel",
				emoji="🐪",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Seems like she was deserted.",
					"He's stuffing his face as usual.",
					"Seems like he was deserted.",
					"She's great on the saxophone.",
					"More specifically, a dromedary.",
				},
				rescue_pair_quotes={
					"That's a camel-lot!",
				},
			),
			AnimalC(
				name="cat",
				displayname="Cat",
				emoji="🐱",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"They have stripes because it's better than being spotted.",
					"You pet her as you celebrate your first moments together.",
					"His name is probably Bessie.",
					"He's stuffing his face as usual.",
					"Though he's just standing there menacingly.",
					"It's off the hook!",
					"She's stuffing her face as usual.",
					"He owns you now!",
					"She owns you now!",
					"Perfect for awkward moments.",
					"The memes cannot be contained.",
					"You pet him as you celebrate your first moments together.",
					"You must be thrilled right now.",
				},
				rescue_pair_quotes={
					"You could make a musical out of this.",
				},
			),
			AnimalC(
				name="caterpillar",
				displayname="Caterpillar",
				emoji="🐛",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She seems hungry.",
					"She's great on the saxophone.",
					"He seems hungry.",
					"He's great on the saxophone.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="chick",
				displayname="Chick",
				emoji="🐥",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"You don't own any deep fryers, right?",
					"And his mother doesn't even care.",
					"...Or, that might just be his tongue.",
					"She chirps with excitement.",
					"He chirps with excitement.",
					"You can find them all over the web.",
					"And her mother doesn't even care.",
					"Now do it in real life.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="chicken",
				displayname="Chicken",
				emoji="🐔",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"You better not play trash.",
					"He performs rock music sometimes.",
					"No egg needed!",
					"Don't do anything unethical.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"A... pair-rot? Sorry.",
					"Lucky you!",
					"Nice going!",
					"Quackers!",
				},
			),
			AnimalC(
				name="cow",
				displayname="Cow",
				emoji="🐄",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"His name is probably Bessie.",
					"What a legendairy find!",
					"Seems crunchy...",
					"More specifically, a dromedary.",
					"I swear I won't milk her for puns.",
					"They have hooves because they lactose.",
					"I swear I won't milk him for puns.",
					"Her name is probably Bessie.",
					"She's a medically trained professional.",
					"Don't leave his tail behind!",
					"They have quite impressive tools.",
				},
				rescue_pair_quotes={
					"They seem to have some beef with each other.",
				},
			),
			AnimalC(
				name="crab",
				displayname="Crab",
				emoji="🦀",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's happy as a clam.",
					"I think she wants your money.",
					"He's happy as a clam.",
					"What the dog doin?",
					"I think he wants your money.",
					"<https://youtu.be/LDU_Txk06tM>",
					"You can finally say you had a good morning.",
					"You can't hide from him forever.",
				},
				rescue_pair_quotes={
					"It's a rave!",
					"Lucky you!",
				},
			),
			AnimalC(
				name="cricket",
				displayname="Cricket",
				emoji="🦗",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"I wonder what her favorite sport is?",
					"Seems crunchy...",
					"She also knows how to dance.",
					"I wonder what his favorite sport is?",
					"He's great on the saxophone.",
					"More specifically, a dromedary.",
					"Perfect for awkward moments.",
				},
				rescue_pair_quotes={
					"Awkward...",
				},
			),
			AnimalC(
				name="crocodile",
				displayname="Crocodile",
				emoji="🐊",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"I think she wants your money.",
					"She's in sport mode.",
					"He's in sport mode.",
					"Your baby daddy's worst nightmare.",
				},
				rescue_pair_quotes={
					"Also referred to a pair of crocs.",
					"Also referred to as a pair of crocs.",
				},
			),
			AnimalC(
				name="deer",
				displayname="Deer",
				emoji="🦌",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He seems quite fawn of you.",
					"She might know ice magic.",
					"She seems quite fawn of you.",
					"This would make for a good anime.",
					"He might know ice magic.",
				},
				rescue_pair_quotes={
					"You could start a deer club!",
				},
			),
			AnimalC(
				name="dinosaur",
				displayname="Dinosaur",
				emoji="🦕",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Shouldn't that be a bigger deal?",
					"And the rest is history.",
					"That happens sometimes.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Nice going!",
					"Am I seriously supposed to believe you have space for this?",
					"Sweet!",
				},
			),
			AnimalC(
				name="dog",
				displayname="Dog",
				emoji="🐶",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's a good girl!",
					"What the dog doin?",
					"\\*nuzzles*",
					"He's a good boy!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Awkward...",
					"Sweet!",
				},
			),
			AnimalC(
				name="dove",
				displayname="Dove",
				emoji="🕊️",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"His friend might know how to drive a bus.",
					"Don't leave her tail behind!",
					"Her friend might know how to drive a bus.",
					"He's fresh out of the shower.",
					"He takes pride in his ear floof.",
					"She's fresh out of the shower.",
					"She's looking awfully like a muffin.",
				},
				rescue_pair_quotes=set(),
			),
			AnimalC(
				name="duck",
				displayname="Duck",
				emoji="🦆",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He appears to enjoy spinning around.",
					"She's bouncing in time to the beat.",
					"She appears to enjoy spinning around.",
					"He offers good advice sometimes.",
					"She offers good advice sometimes.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Quackers!",
					"Lucky you!",
					"Nice going!",
					"Sweet!",
				},
			),
			AnimalC(
				name="elephant",
				displayname="Elephant",
				emoji="🐘",
				an="an",
				rescue_verbs=set(),
				rescue_quotes={
					"She thinks this is the only command.",
					"Not sure how you carried him back but that's not important.",
					"Don't expect your wood to last.",
					"He thinks this is the only command.",
					"Not sure how you carried her back but that's not important.",
					"She's stuffing her face as usual.",
					"He might be able to fit in the fridge.",
					"You can find them all over the web.",
					"She might be able to fit in the fridge.",
					"Wowie zowie!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"They have really, really, really long, um, trunks.",
				},
			),
			AnimalC(
				name="fish",
				displayname="Fish",
				emoji="🐟",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"You can finally say you had a good morning.",
					"She appears to enjoy spinning around.",
					"She chirps with excitement.",
					"It's at least a B+!",
					"She seems to care a lot about justice.",
					"Share it on your dating profile!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="fly",
				displayname="Fly",
				emoji="🪰",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He's not the best limbo player.",
					"\\*nuzzles*",
					"You must be thrilled right now.",
					"Not really something to make a buzz about.",
				},
				rescue_pair_quotes={
					"Gross...",
					"Sweet!",
				},
			),
			AnimalC(
				name="fox",
				displayname="Fox",
				emoji="🦊",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"What a legendairy find!",
					"Please tell others about this!",
					"\\*nuzzles*",
					"Wonder what she sounds like...",
					"Wonder what he sounds like...",
				},
				rescue_pair_quotes={
					"Must be a shrine nearby...",
				},
			),
			AnimalC(
				name="frog",
				displayname="Frog",
				emoji="🐸",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"They're rare to see on the internet.",
					"If you were a Gex fan you'd get that.",
					"You must be thrilled right now.",
					"Oh heck waddup!!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="giraffe",
				displayname="Giraffe",
				emoji="🦒",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's quite giddy about it.",
					"She's not the best limbo player.",
					"He's got quite the view from up there.",
					"They're rare to see on the internet.",
					"He's not the best limbo player.",
					"He's struggling to figure out how to wear a tie.",
					"She's got quite the view from up there.",
					"She's struggling to figure out how to wear a tie.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="gorilla",
				displayname="Gorilla",
				emoji="🦍",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"They peaked in 1897.",
					"She is a quiet gorilla.",
					"He is a quiet gorilla.",
					"She's the leader of the bunch.",
					"Did you hear about the one that escaped from someone's zoo?",
					"He's the leader of the bunch.",
					"Please keep young children away.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"They feel good.",
					"Nice going!",
					"Lucky you!",
				},
			),
			AnimalC(
				name="hamster",
				displayname="Hamster",
				emoji="🐹",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Seems crunchy...",
					"She's bouncing in time to the beat.",
					"What the dog doin?",
					"Not sure how you carried her back but that's not important.",
					"She's looking awfully like a muffin.",
					"He's looking awfully like a muffin.",
					"She's craving chili dogs.",
					"She demands blood and potatoes.",
					"She's mastered the art of camouflage.",
					"He's bouncing in time to the beat.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="hedgehog",
				displayname="Hedgehog",
				emoji="🦔",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's craving chili dogs.",
					"He stole all your shrubberies!",
					"He's craving chili dogs.",
					"She stole all your shrubberies!",
					"More specifically, a dromedary.",
				},
				rescue_pair_quotes={
					"Or maybe one is an echidna.",
				},
			),
			AnimalC(
				name="hippo",
				displayname="Hippo",
				emoji="🦛",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"I think he likes you.",
					"...Or, that might just be her tongue.",
					"She's a medically trained professional.",
					"He's trying to get off the menu.",
					"I think she likes you.",
					"Apparently they have a personal vendetta against flowing water.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="horse",
				displayname="Horse",
				emoji="🐴",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's quite giddy about it.",
					"He's quite giddy about it.",
					"Oh man!",
					"She chirps with excitement.",
					"Why the long face?",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="koala",
				displayname="Koala",
				emoji="🐨",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She knows how to fry rice.",
					"You better not play trash.",
					"Seems crunchy...",
					"He takes pride in his ear floof.",
					"She's one with the trees.",
					"He is a quiet gorilla.",
					"He's one with the trees.",
					"She takes pride in her ear floof.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="leopard",
				displayname="Leopard",
				emoji="🐆",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Don't expect your wood to last.",
					"He's trying to figure out what his tail tastes like.",
					"Shouldn't that be a bigger deal?",
					"She's trying to figure out what her tail tastes like.",
					"He's looking for a worthy opponent.",
					"She's looking for a worthy opponent.",
					"Share it on your dating profile!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="lizard",
				displayname="Lizard",
				emoji="🦎",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He follows whatever everyone else is doing.",
					"Don't leave her tail behind!",
					"If you were a Gex fan you'd get that.",
					"Don't leave his tail behind!",
					"Not really something to make a buzz about.",
				},
				rescue_pair_quotes={
					"Must be Gex night.",
				},
			),
			AnimalC(
				name="mouse",
				displayname="Mouse",
				emoji="🐭",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Please do not plug her in.",
					"Seems like she got addicted to some game that positively reinforces her every six hours.",
					"You don't own any deep fryers, right?",
					"Seems like he got addicted to some game that positively reinforces him every six hours.",
					"Please do not plug him in.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="ox",
				displayname="Ox",
				emoji="🐂",
				an="an",
				rescue_verbs=set(),
				rescue_quotes={
					"You better not play trash.",
					"Better submit a bug report.",
					"He's fresh out of the shower.",
					"She's looking awfully like a muffin.",
					"He's got quite the appetite.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"They seem to have some beef with each other.",
					"Nice going!",
				},
			),
			AnimalC(
				name="parrot",
				displayname="Parrot",
				emoji="🦜",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"a **Parrot**!",
					"He also knows how to dance.",
					"She also knows how to dance.",
					"You stunned him just as he was waking up!",
					"Don't do anything unethical.",
					"You stunned her just as she was waking up!",
					"Perfect for awkward moments.",
				},
				rescue_pair_quotes={
					"A... pair-rot? Sorry.",
				},
			),
			AnimalC(
				name="penguin",
				displayname="Penguin",
				emoji="🐧",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She smiles and waves.",
					"He smiles and waves.",
					"Please do not plug her in.",
					"Please tell others about this!",
					"Your baby daddy's worst nightmare.",
					"We did it, boys.",
				},
				rescue_pair_quotes={
					"Maybe there's two more somewhere?",
				},
			),
			AnimalC(
				name="pig",
				displayname="Pig",
				emoji="🐷",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She demands blood and potatoes.",
					"She's worthy of a crown.",
					"He demands blood and potatoes.",
					"He's worthy of a crown.",
				},
				rescue_pair_quotes={
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="rabbit",
				displayname="Rabbit",
				emoji="🐰",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"That'll hold 'em alright.",
					"He's one with the trees.",
					"She's deadlier than she looks.",
					"He's craving chili dogs.",
					"He's deadlier than he looks.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="seal",
				displayname="Seal",
				emoji="🦭",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He's trying to get off the menu.",
					"Her breath smells like... cement?",
					"Don't leave his tail behind!",
					"His breath smells like... cement?",
					"Foolishly she sits there smiling.",
					"Foolishly he sits there smiling.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="sheep",
				displayname="Sheep",
				emoji="🐑",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He follows whatever everyone else is doing.",
					"Apparently they have a personal vendetta against flowing water.",
					"You can finally say you had a good morning.",
					"A key ingredient for settlements.",
					"She follows whatever everyone else is doing.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="shrimp",
				displayname="Shrimp",
				emoji="🦐",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She knows how to fry rice.",
					"They have stripes because it's better than being spotted.",
					"I think she wants your money.",
					"He knows how to fry rice.",
					"She owns you now!",
					"Not really something to make a buzz about.",
				},
				rescue_pair_quotes={
					"Nice going!",
					'There\'s no "I" in "prawn"!',
				},
			),
			AnimalC(
				name="skunk",
				displayname="Skunk",
				emoji="🦨",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Maybe keep her away from the other animals.",
					"He's bouncing in time to the beat.",
					"Please keep dogs away.",
					"He slowly approaches.",
					"Maybe keep him away from the other animals.",
					"Not really something to make a buzz about.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="sloth",
				displayname="Sloth",
				emoji="🦥",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Sounds delicious!",
					"He's bouncing in time to the beat.",
					"He's almost as slow as my ping!",
					"Check out his Minecraft server.",
					"She's almost as slow as my ping!",
					"Check out her Minecraft server.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="snail",
				displayname="Snail",
				emoji="🐌",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's worthy of a crown.",
					"She thinks the cooldown should be longer.",
					"You can't hide from him forever.",
					"You can't hide from her forever.",
					"He's worthy of a crown.",
					"He thinks the cooldown should be longer.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"You're on a roll!",
					"Nice going!",
					"Sweet!",
				},
			),
			AnimalC(
				name="spider",
				displayname="Spider",
				emoji="🕷️",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He's mastered the art of camoflauge.",
					"You can find them all over the web.",
					"She's a medically trained professional.",
					"He's mastered the art of camouflage.",
					"She's mastered the art of camouflage.",
					"He's a medically trained professional.",
					"She's mastered the art of camoflauge.",
				},
				rescue_pair_quotes=set(),
			),
			AnimalC(
				name="squid",
				displayname="Squid",
				emoji="🦑",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"He does not know how to handle firearms.",
					"She follows whatever everyone else is doing.",
					"It's off the hook!",
					"The doom of humanity.",
					"I think he wants your money.",
					"She does not know how to handle firearms.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="turkey",
				displayname="Turkey",
				emoji="🦃",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"She's trying to get off the menu.",
					"He's trying to get off the menu.",
					"They're trying to get off the menu.",
					"You promised him plenty of stuff.",
					"You don't own any deep fryers, right?",
					"What the dog doin?",
					"You promised her plenty of stuff.",
				},
				rescue_pair_quotes={
					"Those are some... angry birds.",
				},
			),
			AnimalC(
				name="whale",
				displayname="Whale",
				emoji="🐳",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"Seems crunchy...",
					"Where are you even going to put her?",
					"It's off the hook!",
					"She's got quite the appetite.",
					"Where are you even going to put him?",
					"He's got quite the appetite.",
				},
				rescue_pair_quotes={
					"Am I seriously supposed to believe you have space for this?",
				},
			),
			AnimalC(
				name="worm",
				displayname="Worm",
				emoji="🪱",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"...Or, that might just be her tongue.",
					"She offers good advice sometimes.",
					"He's bouncing in time to the beat.",
					"...Or, that might just be his tongue.",
					"It's on the hook!",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Lucky you!",
					"Sweet!",
					"Nice going!",
				},
			),
			AnimalC(
				name="zebra",
				displayname="Zebra",
				emoji="🦓",
				an="a",
				rescue_verbs=set(),
				rescue_quotes={
					"They have stripes because it's better than being spotted.",
					"He performs rock music sometimes.",
					"Put down the barcode scanner.",
					"If you were a Gex fan you'd get that.",
				},
				rescue_pair_quotes={
					"How lucky!",
					"Maybe there's two more somewhere?",
					"Lucky you!",
					"Sweet!",
				},
			),
		)
	}

	RARE_ANIMALS: dict[str, AnimalR] = {
		animal.name: animal
		for animal in (
			AnimalR(
				name="bactrian camel",
				displayname="Bactrian Camel",
				emoji="🐫",
				an="a",
				exchange_quotes={
					"Room for more passengers!",
					"What an upgrade!",
				},
			),
			AnimalR(
				name="badger",
				displayname="Badger",
				emoji="🦡",
				an="a",
				exchange_quotes={
					"That's pretty sweet.",
				},
			),
			AnimalR(
				name="bee",
				displayname="Bee",
				emoji="🐝",
				an="a",
				exchange_quotes={
					"Her wings are too small to get her fat little body off the ground.",
					"He got over here rather quickly.",
					"Stand back, these are winter boots.",
					"His wings are too small to get his fat little body off the ground.",
				},
			),
			AnimalR(
				name="bird",
				displayname="Bird",
				emoji="🐦",
				an="a",
				exchange_quotes={
					"What kind? I'm not the person to ask.",
					"At least, that's what the government wants you to think.",
				},
			),
			AnimalR(
				name="bison",
				displayname="Bison",
				emoji="🦬",
				an="a",
				exchange_quotes={
					"I say that every night.",
					"(bye dad!)",
				},
			),
			AnimalR(
				name="boar",
				displayname="Boar",
				emoji="🐗",
				an="a",
				exchange_quotes={
					"What a mind-blowing deal!",
					"600-500 BC, Etruscan, ceramic.",
				},
			),
			AnimalR(
				name="bunny",
				displayname="Bunny",
				emoji="🐇",
				an="a",
				exchange_quotes={
					"Let's just pretend there's a difference.",
					"Bnuuy!!",
				},
			),
			AnimalR(
				name="butterfly",
				displayname="Butterfly",
				emoji="🦋",
				an="a",
				exchange_quotes={
					"That's how nature works.",
					"Better than a moth, I guess.",
				},
			),
			AnimalR(
				name="chipmunk",
				displayname="Chipmunk",
				emoji="🐿",
				an="a",
				exchange_quotes={
					"He invented nightcore.",
					"She sings 2010s music sometimes.",
					"He sings 2010s music sometimes.",
					"She invented nightcore.",
				},
			),
			AnimalR(
				name="cockroach",
				displayname="Cockroach",
				emoji="🪳",
				an="a",
				exchange_quotes={
					"...and there will probably be more to come.",
				},
			),
			AnimalR(
				name="dodo",
				displayname="Dodo",
				emoji="🦤",
				an="a",
				exchange_quotes={
					"How'd you pull that one off?",
				},
			),
			AnimalR(
				name="dolphin",
				displayname="Dolphin",
				emoji="🐬",
				an="a",
				exchange_quotes={
					"He might be smarter than you.",
					"She might be smarter than you.",
					"She knows 13 bad words.",
					"Flipper? More like, 'Sipper... of tropical drinks!",
				},
			),
			AnimalR(
				name="donkey",
				displayname="Donkey",
				emoji="🫏",
				an="a",
				exchange_quotes={
					"She wants to review your video games.",
				},
			),
			AnimalR(
				name="dragon",
				displayname="Dragon",
				emoji="🐲",
				an="a",
				exchange_quotes={
					"That's actually pretty cool.",
					"He's yet to be trained.",
					"She's yet to be trained.",
				},
			),
			AnimalR(
				name="eagle",
				displayname="Eagle",
				emoji="🦅",
				an="an",
				exchange_quotes={
					"How patriotic!",
					"He has no idea what a kilometer is.",
				},
			),
			AnimalR(
				name="flamingo",
				displayname="Flamingo",
				emoji="🦩",
				an="a",
				exchange_quotes={
					"He's showing off his natural hue.",
					"She's showing off her natural hue.",
				},
			),
			AnimalR(
				name="goat",
				displayname="Goat",
				emoji="🐐",
				an="a",
				exchange_quotes={
					"You should have switched to the other door.",
					"This is the greatest trade deal of All Time.",
					"Absolutely goated decision.",
				},
			),
			AnimalR(
				name="jellyfish",
				displayname="Jellyfish",
				emoji="🪼",
				an="a",
				exchange_quotes={
					"Shocking, isn't it?",
					"He's already started jamming.",
					"She's already started jamming.",
				},
			),
			AnimalR(
				name="kangaroo",
				displayname="Kangaroo",
				emoji="🦘",
				an="a",
				exchange_quotes={
					"She's upside down for some reason.",
					"He's upside down for some reason.",
				},
			),
			AnimalR(
				name="ladybug",
				displayname="Ladybug",
				emoji="🐞",
				an="a",
				exchange_quotes={
					"Ironically, this one seems to be male.",
					"Treat her nicely!",
				},
			),
			AnimalR(
				name="lion",
				displayname="Lion",
				emoji="🦁",
				an="a",
				exchange_quotes={
					"Only 999,999,999 more to go.",
					"The star of everyone's favorite biblical adventure!",
					"Everything the light touches belongs to him. (except for that shadowy blue bot)",
					"He'll build up courage some day.",
					"Everything the light touches belongs to her. (except for that shadowy blue bot)",
					"She'll build up courage some day.",
				},
			),
			AnimalR(
				name="llama",
				displayname="Llama",
				emoji="🦙",
				an="a",
				exchange_quotes={
					"Don't throw off her groove!",
					"Or maybe it's an alpaca, Emojipedia says either.",
					"Don't throw off his groove!",
					"He's upside down for some reason.",
				},
			),
			AnimalR(
				name="lobster",
				displayname="Lobster",
				emoji="🦞",
				an="a",
				exchange_quotes={
					"Looks like it wasn't a rock!",
					"You do not control the speed at which she dies.",
					"You do not control the speed at which he dies.",
					"How long until he evolves back into a crab?",
					"How long until she evolves back into a crab?",
				},
			),
			AnimalR(
				name="mammoth",
				displayname="Mammoth",
				emoji="🦣",
				an="a",
				exchange_quotes={
					"I guess there's still a couple left.",
				},
			),
			AnimalR(
				name="monkey",
				displayname="Monkey",
				emoji="🐒",
				an="a",
				exchange_quotes={
					"His life could be a dream.",
					"Feel free to screenshot.",
					"Her life could be a dream.",
				},
			),
			AnimalR(
				name="moose",
				displayname="Moose",
				emoji="🫎",
				an="a",
				exchange_quotes={
					"Don't set her loose!",
					"Don't set him loose!",
				},
			),
			AnimalR(
				name="mosquito",
				displayname="Mosquito",
				emoji="🦟",
				an="a",
				exchange_quotes={
					"What is wrong with you??",
					"You're part of the problem now.",
				},
			),
			AnimalR(
				name="octopus",
				displayname="Octopus",
				emoji="🐙",
				an="an",
				exchange_quotes={
					"All the kids are scared of his name.",
					"The tentacles are off limits.",
					"All the kids are scared of her name.",
				},
			),
			AnimalR(
				name="orangutan",
				displayname="Orangutan",
				emoji="🦧",
				an="an",
				exchange_quotes={
					"Uh oh!!",
					"In other words, you got big monke",
				},
			),
			AnimalR(
				name="otter",
				displayname="Otter",
				emoji="🦦",
				an="an",
				exchange_quotes={
					"Just wait until her birthday.",
					"They're just cuter.",
					"Just wait until his birthday.",
				},
			),
			AnimalR(
				name="owl",
				displayname="Owl",
				emoji="🦉",
				an="an",
				exchange_quotes={
					"Though he doesn't look like a very *happy* owl.",
					"(augh)",
					"He's not accepting your other animals.",
					"Keep the bugs away.",
					"Though she doesn't look like a very *happy* owl.",
					"She's not accepting your other animals.",
				},
			),
			AnimalR(
				name="panda",
				displayname="Panda",
				emoji="🐼",
				an="a",
				exchange_quotes={
					"Who wouldn't?",
					"Call that Panda Express.",
				},
			),
			AnimalR(
				name="peacock",
				displayname="Peacock",
				emoji="🦚",
				an="a",
				exchange_quotes={
					"You say its name and no one bats an eye, but...",
				},
			),
			AnimalR(
				name="polar bear",
				displayname="Polar Bear",
				emoji="🐻\u200d❄️",
				an="a",
				exchange_quotes={
					"I don't think she likes the penguins.",
					"I don't think he likes the penguins.",
					"He might be smarter than you.",
				},
			),
			AnimalR(
				name="poodle",
				displayname="Poodle",
				emoji="🐩",
				an="a",
				exchange_quotes={
					"And all it took was a few baguettes.",
					"You say its name and no one bats an eye, but...",
					"What a mind-blowing deal!",
				},
			),
			AnimalR(
				name="pufferfish",
				displayname="Pufferfish",
				emoji="🐡",
				an="a",
				exchange_quotes={
					"(augh)",
					"<('O')>",
				},
			),
			AnimalR(
				name="raccoon",
				displayname="Raccoon",
				emoji="🦝",
				an="a",
				exchange_quotes={
					"Not to be confused with a tanuki.",
					"Flight powers not included.",
				},
			),
			AnimalR(
				name="ram",
				displayname="Ram",
				emoji="🐏",
				an="a",
				exchange_quotes={
					"A great alternative to human sacrifice.",
					"His sister is nicer though.",
					"You can probably download even more!",
					"Her sister is nicer though.",
				},
			),
			AnimalR(
				name="rat",
				displayname="Rat",
				emoji="🐀",
				an="a",
				exchange_quotes={
					"Maybe he'll cook you dinner.",
					"Maybe she'll cook you dinner.",
					"He might make you crazy.",
					"The tentacles are off limits.",
					"They prey and stalk at night.",
					"She might make you crazy.",
				},
			),
			AnimalR(
				name="rhino",
				displayname="Rhino",
				emoji="🦏",
				an="a",
				exchange_quotes={
					"She's real proud of her horns.",
					"She gets a little philosophical sometimes.",
					"He's real proud of his horns.",
				},
			),
			AnimalR(
				name="rooster",
				displayname="Rooster",
				emoji="🐓",
				an="a",
				exchange_quotes={
					"You say its name and no one bats an eye, but...",
					"You had enough eggs anyways.",
					"Don't do anything fowl.",
				},
			),
			AnimalR(
				name="scorpion",
				displayname="Scorpion",
				emoji="🦂",
				an="a",
				exchange_quotes={
					"He got over here rather quickly.",
					"She got over here rather quickly.",
				},
			),
			AnimalR(
				name="shark",
				displayname="Shark",
				emoji="🦈",
				an="a",
				exchange_quotes={
					"He lets out a mighty 'a'.",
					"No, he will not date you.",
					"She lets out a mighty 'a'.",
					"No, she will not date you.",
				},
			),
			AnimalR(
				name="snake",
				displayname="Snake",
				emoji="🐍",
				an="a",
				exchange_quotes={
					"Try to avoid the walls.",
					"Her head is smol but jaw is stronk.",
					"His head is smol but jaw is stronk.",
				},
			),
			AnimalR(
				name="swan",
				displayname="Swan",
				emoji="🦢",
				an="a",
				exchange_quotes={
					"Better choice than a goose.",
				},
			),
			AnimalR(
				name="t-rex",
				displayname="T-Rex",
				emoji="🦖",
				an="a",
				exchange_quotes={
					"You might want to fix your internet connection.",
					"You might wanna fix your internet connection.",
				},
			),
			AnimalR(
				name="tiger",
				displayname="Tiger",
				emoji="🐯",
				an="a",
				exchange_quotes={
					"Room for more passengers!",
					"Let's go golfing!",
					"He gets a little philosophical sometimes.",
					"She gets a little philosophical sometimes.",
					"How'd you pull that one off?",
				},
			),
			AnimalR(
				name="turtle",
				displayname="Turtle",
				emoji="🐢",
				an="a",
				exchange_quotes={
					"I wonder what she's selling?",
					"Everyone's favorite emoji.",
					"I wonder what he's selling?",
					"Or... maybe it's a tortoise?",
				},
			),
			AnimalR(
				name="unicorn",
				displayname="Unicorn",
				emoji="🦄",
				an="a",
				exchange_quotes={
					"Why do they have a horn?",
					"How magical!",
				},
			),
			AnimalR(
				name="wolf",
				displayname="Wolf",
				emoji="🐺",
				an="a",
				exchange_quotes={
					"He could use some more muscle.",
					"Her sharp teeth are better to eat you with.",
					"She could use some more muscle.",
					"She's already started jamming.",
					"His sharp teeth are better to eat you with.",
				},
			),
		)
	}

	ANIMALS: dict[str, Animal] = COMMON_ANIMALS | RARE_ANIMALS

	COMMON_TO_RARE_MAPPING = {
		COMMON_ANIMALS["fox"].name: RARE_ANIMALS["wolf"].name,
		COMMON_ANIMALS["worm"].name: RARE_ANIMALS["snake"].name,
		COMMON_ANIMALS["beetle"].name: RARE_ANIMALS["ladybug"].name,
		COMMON_ANIMALS["lizard"].name: RARE_ANIMALS["dragon"].name,
		COMMON_ANIMALS["fish"].name: RARE_ANIMALS["jellyfish"].name,
		COMMON_ANIMALS["frog"].name: RARE_ANIMALS["turtle"].name,
		COMMON_ANIMALS["giraffe"].name: RARE_ANIMALS["kangaroo"].name,
		COMMON_ANIMALS["koala"].name: RARE_ANIMALS["raccoon"].name,
		COMMON_ANIMALS["pig"].name: RARE_ANIMALS["boar"].name,
		COMMON_ANIMALS["turkey"].name: RARE_ANIMALS["dodo"].name,
		COMMON_ANIMALS["duck"].name: RARE_ANIMALS["swan"].name,
		COMMON_ANIMALS["parrot"].name: RARE_ANIMALS["peacock"].name,
		COMMON_ANIMALS["penguin"].name: RARE_ANIMALS["polar bear"].name,
		COMMON_ANIMALS["chick"].name: RARE_ANIMALS["bird"].name,
		COMMON_ANIMALS["spider"].name: RARE_ANIMALS["scorpion"].name,
		COMMON_ANIMALS["crab"].name: RARE_ANIMALS["lobster"].name,
		COMMON_ANIMALS["leopard"].name: RARE_ANIMALS["lion"].name,
		COMMON_ANIMALS["whale"].name: RARE_ANIMALS["shark"].name,
		COMMON_ANIMALS["horse"].name: RARE_ANIMALS["unicorn"].name,
		COMMON_ANIMALS["skunk"].name: RARE_ANIMALS["badger"].name,
		COMMON_ANIMALS["squid"].name: RARE_ANIMALS["octopus"].name,
		COMMON_ANIMALS["deer"].name: RARE_ANIMALS["moose"].name,
		COMMON_ANIMALS["dove"].name: RARE_ANIMALS["eagle"].name,
		COMMON_ANIMALS["cricket"].name: RARE_ANIMALS["cockroach"].name,
		COMMON_ANIMALS["crocodile"].name: RARE_ANIMALS["pufferfish"].name,
		COMMON_ANIMALS["hippo"].name: RARE_ANIMALS["rhino"].name,
		COMMON_ANIMALS["mouse"].name: RARE_ANIMALS["rat"].name,
		COMMON_ANIMALS["beaver"].name: RARE_ANIMALS["otter"].name,
		COMMON_ANIMALS["hedgehog"].name: RARE_ANIMALS["donkey"].name,
		COMMON_ANIMALS["shrimp"].name: RARE_ANIMALS["flamingo"].name,
		COMMON_ANIMALS["hamster"].name: RARE_ANIMALS["chipmunk"].name,
		COMMON_ANIMALS["sheep"].name: RARE_ANIMALS["ram"].name,
		COMMON_ANIMALS["bat"].name: RARE_ANIMALS["owl"].name,
		COMMON_ANIMALS["ox"].name: RARE_ANIMALS["bison"].name,
		COMMON_ANIMALS["snail"].name: RARE_ANIMALS["bee"].name,
		COMMON_ANIMALS["seal"].name: RARE_ANIMALS["dolphin"].name,
		COMMON_ANIMALS["chicken"].name: RARE_ANIMALS["rooster"].name,
		COMMON_ANIMALS["dog"].name: RARE_ANIMALS["poodle"].name,
		COMMON_ANIMALS["elephant"].name: RARE_ANIMALS["mammoth"].name,
		COMMON_ANIMALS["gorilla"].name: RARE_ANIMALS["orangutan"].name,
		COMMON_ANIMALS["sloth"].name: RARE_ANIMALS["monkey"].name,
		COMMON_ANIMALS["camel"].name: RARE_ANIMALS["bactrian camel"].name,
		COMMON_ANIMALS["zebra"].name: RARE_ANIMALS["llama"].name,
		COMMON_ANIMALS["bear"].name: RARE_ANIMALS["panda"].name,
		COMMON_ANIMALS["fly"].name: RARE_ANIMALS["mosquito"].name,
		COMMON_ANIMALS["rabbit"].name: RARE_ANIMALS["bunny"].name,
		COMMON_ANIMALS["caterpillar"].name: RARE_ANIMALS["butterfly"].name,
		COMMON_ANIMALS["cow"].name: RARE_ANIMALS["goat"].name,
		COMMON_ANIMALS["dinosaur"].name: RARE_ANIMALS["t-rex"].name,
		COMMON_ANIMALS["cat"].name: RARE_ANIMALS["tiger"].name,
	}

	RARE_TO_COMMON_MAPPING = {v: k for k, v in COMMON_TO_RARE_MAPPING.items()}

	if any(common not in COMMON_TO_RARE_MAPPING for common in COMMON_ANIMALS):
		raise RuntimeError("Not all common animals have a to-rare mapping defined\n" + str(COMMON_ANIMALS - set(COMMON_TO_RARE_MAPPING)))

	if any(rare not in RARE_TO_COMMON_MAPPING for rare in RARE_ANIMALS):
		raise RuntimeError(f"Not all rare animals have a to-common mapping defined\n" + str(RARE_ANIMALS - set(RARE_TO_COMMON_MAPPING)))

	logger = get_logger(__name__)

	logger.info(f"loaded {len(COMMON_ANIMALS)} common and {len(RARE_ANIMALS)} rare animal statics ({len(ANIMALS)} total).")
