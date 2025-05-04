import random
from typing import Self

from common import ACL
from prelude import *

from .._version import __version__
from ..db import User, UserDB
from ..lang import LANG
from ..models.animal import COMMON_ANIMALS, AnimalC


class Rescue(ZooBM):
	ctx: arc.GatewayContext
	user: User

	animal: AnimalC
	is_pair: bool

	@classmethod
	async def from_ctx_user(cls, *, ctx: arc.GatewayContext, user: User) -> Self:
		chosen_animal_name = random.choice((*COMMON_ANIMALS,))  # TODO: calculate based on user & events

		pair_chance = 0.05  # TODO: calculate based on user & events

		return cls(
			ctx=ctx,
			user=user,
			animal=AnimalC.from_name(chosen_animal_name),
			is_pair=pair_chance > random.random(),
		)

	async def _make_first_line(self) -> str:
		return (
			f"{self.animal.emoji * (2 if self.is_pair else 1)}"  # ("ruff, dont fold the multiline string" comment)
			f" You {self.animal.get_random_rescue_verb()} {self.animal.an} **{self.animal.displayname}**!"
			f"{f' {self.animal.get_random_rescue_quote(is_pair=self.is_pair).lstrip()}'.rstrip()}"
		)

	async def _make_lines(self) -> list[str]:
		return [await self._make_first_line()]

	async def to_str(self) -> str:
		return "\n".join(await self._make_lines())


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.rescue"))
async def cmd_rescue(ctx: arc.GatewayContext) -> None:
	with UserDB(ctx.author.id) as user:
		rescue = await Rescue.from_ctx_user(ctx=ctx, user=user)

		await (await user.ensure_profile(ctx)).apply_rescue(rescue)

		await ctx.respond(await rescue.to_str())
