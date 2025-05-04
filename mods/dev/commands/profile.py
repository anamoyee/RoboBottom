from _.config import S
from _.db import UserDB
from _.db.model_profile import ProfileID
from _.tools import OPTION_EPHEMERAL, ephemeral_from_bool
from prelude import *
from tcrutils import discord_ifys as IFYs
from tcrutils.codeblock import codeblock
from tcrutils.print import fmt_iterable

from ._base import GROUP_DEV


async def autocomplete_profile(data: arc.AutocompleteData) -> list[str]:
	options_dict = {option.name: option for option in data.options}

	account_option_value = options_dict.get["account"].value if "account" in options_dict else data.interaction.user.id

	if account_option_value not in UserDB:
		return []

	with UserDB(account_option_value) as acc:
		return [profile.id.value for profile in acc.profiles]


@GROUP_DEV.include
@arc.slash_subcommand("profile", "View a raw profile data from the database.")
async def cmd_dev_profile(
	ctx: arc.GatewayContext,
	account: arc.Option[int | None, arc.IntParams("Account ID (default: this account)")] = None,
	profile_name: arc.Option[str | None, arc.StrParams("Profile ID (default: entire account, not just profile)", name="profile", autocomplete_with=autocomplete_profile)] = None,
	ephemeral: OPTION_EPHEMERAL = True,
):
	account = account if account is not None else ctx.user.id

	flags = ephemeral_from_bool(ephemeral)

	account_text = f"{IFYs.userify(account)} (`{account}`)"

	if account not in UserDB:
		await ctx.respond(f"{S.NO} Unknown account {account_text}", user_mentions=[], flags=flags)
		return

	with UserDB(account) as acc:
		if not acc.profiles:
			await ctx.respond(f"{S.NO} Account {account_text} has no profiles", user_mentions=[], flags=flags)
			return

		if profile_name is None:
			await ctx.respond(
				codeblock(fmt_iterable(acc), langcode="py"),
				flags=flags,
			)
			return

		profile_name = profile_name.lower()

		try:
			profile_name_enumed = ProfileID(profile_name)
		except ValueError:
			await ctx.respond(f"{S.NO} Invalid profile `{profile_name}`", flags=flags)
			return

		profile = acc.profiles.get(profile_name_enumed)

		if profile is None:
			await ctx.respond(f"{S.NO} Account {account_text} doesn't have a `{profile_name_enumed}` profile", user_mentions=[], flags=flags)
			return

		await ctx.respond(
			codeblock(fmt_iterable(profile), langcode="py"),
			flags=flags,
		)
		return
