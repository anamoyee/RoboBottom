from ._base import *

if True:  # types

	class Item(HasEmoji):
		"""Ownerless item representation, if owned, will be included as a mapping of items: `dict[Item.name: str, amount: int]`."""

		name: str
		"""The (internal, not display) name of this item."""

		displayname: str
		"""The displayname of this item."""

		description: str
		"""The description of this item."""

		quality: int = 1
		"""Numeric quality of this item, generally 1-4, though it technically could be altered by mods to be any integer."""

		sellable: bool = True
		"""Whether or not this item is able to be sold in the shop."""
		purchasable: bool = True
		"""Whether or not this item is able to be purchased from the shop."""

		special: bool = False
		"""Whether or not this item is displayed in blue in lists, the website, etc."""

		no_dms: bool = False
		"""Whether or not this item is prohibited from being used in DMs."""

		tooltip: str = "<Tooltip unset>"
		"""The tooltip of this item."""


if True:  # instances
	ITEMS: dict[str, Item] = {
		item.name: item
		for item in (
			Item(
				name="cookie",
				displayname="Cookie",
				emoji="🍪",
				description="Reduces your current rescue cooldown by 1 hour.",
				quality=1,
			),
			Item(
				name="pizza",
				displayname="Pizza",
				emoji="🍕",
				description="Reduces your current rescue cooldown by 2 hours.",
				quality=2,
			),
			Item(
				name="coffee",
				displayname="Coffee",
				emoji="☕",
				description="Reduces your current rescue cooldown by 4 hours.",
				quality=3,
			),
		)
	}
