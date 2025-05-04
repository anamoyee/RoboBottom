from _.config import S
from _.db import GlobalDB, UserDB, VersionDB
from _.lang import LANG
from _.tools import OPTION_CONFIRM_BOOL, OPTION_CONFIRM_YES_DO_AS_I_SAY, OPTION_EPHEMERAL, OPTION_EXISTS_CHECK, OPTION_TO_FILE, ephemeral_from_bool
from prelude import *
from tcrutils.language import plural_s

from ._base import GROUP_DEV

GROUP_DEV_CLEARDB = GROUP_DEV.include_subgroup(**LANG.get_arc_command("/.dev_cleardb"))

if True:  # Users

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_user"))
	async def cmd_dev_cleardb_user(
		ctx: arc.GatewayContext,
		user: arc.Option[hikari.User, arc.UserParams(**LANG.get_arc_command("/.dev_cleardb_user:user"))],
		ephemeral: OPTION_EPHEMERAL = True,
		exists_check: OPTION_EXISTS_CHECK = True,
		confirm: OPTION_CONFIRM_BOOL = False,
	) -> None:
		if not confirm:
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option, aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		if exists_check and not UserDB.contains(user.id):
			return await ctx.respond(f"{S.NO} That user is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		try:
			UserDB.delitem_unchecked(user.id)
		except KeyError:
			pass

		await ctx.respond(f"{S.YES} Done!", flags=ephemeral_from_bool(ephemeral))

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_userid"))
	async def cmd_dev_cleardb_userid(
		ctx: arc.GatewayContext,
		user_id: arc.Option[int, arc.IntParams(**LANG.get_arc_command("/.dev_cleardb_userid:user_id"))],
		ephemeral: OPTION_EPHEMERAL = True,
		exists_check: OPTION_EXISTS_CHECK = True,
		confirm: OPTION_CONFIRM_BOOL = False,
	) -> None:
		if not confirm:
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option, aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		if exists_check and not UserDB.contains(user_id):
			return await ctx.respond(f"{S.NO} That user is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		try:
			UserDB.delitem_unchecked(user_id)
		except KeyError:
			pass

		await ctx.respond(f"{S.YES} Done!", flags=ephemeral_from_bool(ephemeral))

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_users"))
	async def cmd_dev_cleardb_users(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		confirm: OPTION_CONFIRM_YES_DO_AS_I_SAY = "",
	) -> None:
		if confirm != "Yes, do as I say!":
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option (read description carefully!), aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		with UserDB.open_shelf() as shelf:
			records = len(shelf)

			shelf.clear()

		await ctx.respond(f"{S.YES} Done! (deleted {records} record{plural_s(records)})", flags=ephemeral_from_bool(ephemeral))


if True:  # Versions

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_version"))
	async def cmd_dev_cleardb_version(
		ctx: arc.GatewayContext,
		version: arc.Option[str, arc.StrParams(**LANG.get_arc_command("/.dev_cleardb_version:version"))],
		ephemeral: OPTION_EPHEMERAL = True,
		exists_check: OPTION_EXISTS_CHECK = True,
		confirm: OPTION_CONFIRM_BOOL = "",
	) -> None:
		if not confirm:
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option, aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		if exists_check and not VersionDB.contains(version):
			return await ctx.respond(f"{S.NO} That version is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		try:
			VersionDB.delitem_unchecked(version)
		except KeyError:
			pass

		await ctx.respond(f"{S.YES} Done!", flags=ephemeral_from_bool(ephemeral))

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_versions"))
	async def cmd_dev_cleardb_versions(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		confirm: OPTION_CONFIRM_YES_DO_AS_I_SAY = "",
	) -> None:
		if confirm != "Yes, do as I say!":
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option (read description carefully!), aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		with VersionDB.open_shelf() as shelf:
			records = len(shelf)

			shelf.clear()

		await ctx.respond(f"{S.YES} Done! (deleted {records} record{plural_s(records)})", flags=ephemeral_from_bool(ephemeral))


if True:  # Global

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_global"))
	async def cmd_dev_cleardb_global(
		ctx: arc.GatewayContext,
		global_: arc.Option[str, arc.StrParams(**LANG.get_arc_command("/.dev_cleardb_global:global"))],
		ephemeral: OPTION_EPHEMERAL = True,
		exists_check: OPTION_EXISTS_CHECK = True,
		confirm: OPTION_CONFIRM_BOOL = "",
	) -> None:
		if not confirm:
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option, aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		if exists_check and not VersionDB.contains(global_):
			return await ctx.respond(f"{S.NO} That global is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		try:
			VersionDB.delitem_unchecked(global_)
		except KeyError:
			pass

		await ctx.respond(f"{S.YES} Done!", flags=ephemeral_from_bool(ephemeral))

	@GROUP_DEV_CLEARDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_cleardb_globals"))
	async def cmd_dev_cleardb_globals(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		confirm: OPTION_CONFIRM_YES_DO_AS_I_SAY = "",
	) -> None:
		if confirm != "Yes, do as I say!":
			return await ctx.respond(f"{S.NO} You must confirm this action with `confirm` option (read description carefully!), aborting...", flags=hikari.MessageFlag.EPHEMERAL)

		with GlobalDB() as value:
			records = len(value)

			value.clear()

		await ctx.respond(f"{S.YES} Done! (deleted {records} record{plural_s(records)})", flags=ephemeral_from_bool(ephemeral))
