import datetime

from common import ACL, MCL
from prelude import *

from .._version import __version__
from ..config import S
from ..db import UserDB
from ..lang import LANG
from ..view.nav import LinesPagedView


@ACL.include
@arc.slash_command(**LANG.get_arc_command("/.animals"))
async def cmd_animals(ctx: arc.GatewayContext) -> None:
	with UserDB(ctx.author.id) as user:
		profile = await user.ensure_profile(ctx)

		if not profile.animals:
			await ctx.respond(f"Try rescuing some animals first! (/rescue)", flags=hikari.MessageFlag.EPHEMERAL)
			return

	embed_from_description_fn = lambda description, i, ii: (
		hikari.Embed(
			description=description,
			color=S.COLOR.PRIMARY,
		)
		.set_author(
			name=profile.name,
			icon=ctx.author.avatar_url,
		)
		.set_footer(
			f"Page {i + 1} of {ii}" if ii > 1 else None,
		)
	)

	owned_animal_pairs = sorted(profile.fetch_owned_animals().values(), key=lambda pair: pair[0].name)

	lines = [animal.str_listitem(count=count, loopback_link_ctx=ctx) for (animal, count) in owned_animal_pairs]

	lp_view = LinesPagedView(
		lines,
		n=12,
		embed_from_description_fn=embed_from_description_fn,
	)

	await lp_view.respnd_via_context(ctx=ctx, mcl=MCL)
