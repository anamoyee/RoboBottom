from _.config import S
from _.db import GlobalDB, UserDB, VersionDB
from _.lang import LANG
from _.tools import OPTION_EPHEMERAL, OPTION_EXISTS_CHECK, OPTION_TO_FILE, dump_respond
from prelude import *

from ._base import GROUP_DEV

GROUP_DEV_DUMPDB = GROUP_DEV.include_subgroup(**LANG.get_arc_command("/.dev_dumpdb"))


if True:  # Users

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_user"))
	async def cmd_dev_dumpdb_user(
		ctx: arc.GatewayContext,
		user: arc.Option[hikari.User, arc.UserParams(**LANG.get_arc_command("/.dev_dumpdb_user:user"))],
		ephemeral: OPTION_EPHEMERAL = True,
		exists_check: OPTION_EXISTS_CHECK = True,
		to_file: OPTION_TO_FILE = True,
	) -> None:
		if exists_check and not UserDB.contains(user.id):
			return await ctx.respond(f"{S.NO} That user is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		with UserDB(user.id) as dbuser:
			await dump_respond((user.id, dbuser), ctx=ctx, ephemeral=ephemeral, to_file=to_file)

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_userid"))
	async def cmd_dev_dumpdb_userid(
		ctx: arc.GatewayContext,
		user_id: arc.Option[int, arc.IntParams(**LANG.get_arc_command("/.dev_dumpdb_userid:user_id"))],
		ephemeral: OPTION_EPHEMERAL = True,
		to_file: OPTION_TO_FILE = True,
		exists_check: OPTION_EXISTS_CHECK = True,
	) -> None:
		if exists_check and not UserDB.contains(user_id):
			return await ctx.respond(f"{S.NO} That user is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		with UserDB(user_id) as dbuser:
			await dump_respond((user_id, dbuser), ctx=ctx, ephemeral=ephemeral, to_file=to_file)

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_users"))
	async def cmd_dev_dumpdb_users(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		to_file: OPTION_TO_FILE = True,
	) -> None:
		with UserDB.open_shelf() as shelf:
			await dump_respond(*shelf.items(), ctx=ctx, ephemeral=ephemeral, to_file=to_file)


if True:  # Versions

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_version"))
	async def cmd_dev_dumpdb_version(
		ctx: arc.GatewayContext,
		version: arc.Option[str, arc.StrParams(**LANG.get_arc_command("/.dev_dumpdb_version:version"))],
		ephemeral: OPTION_EPHEMERAL = True,
		to_file: OPTION_TO_FILE = True,
		exists_check: OPTION_EXISTS_CHECK = True,
	) -> None:
		if exists_check and not VersionDB.contains(version):
			return await ctx.respond(f"{S.NO} That version is not present in the database.", flags=hikari.MessageFlag.EPHEMERAL)

		with VersionDB(version) as dbversion:
			await dump_respond((version, dbversion), ctx=ctx, ephemeral=ephemeral, to_file=to_file)

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_versions"))
	async def cmd_dev_dumpdb_versions(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		to_file: OPTION_TO_FILE = True,
	) -> None:
		with VersionDB.open_shelf() as shelf:
			await dump_respond(*shelf.items(), ctx=ctx, ephemeral=ephemeral, to_file=to_file)


if True:  # Global

	@GROUP_DEV_DUMPDB.include
	@arc.slash_subcommand(**LANG.get_arc_command("/.dev_dumpdb_globals"))
	async def cmd_dev_dumpdb_globals(
		ctx: arc.GatewayContext,
		ephemeral: OPTION_EPHEMERAL = True,
		to_file: OPTION_TO_FILE = True,
	) -> None:
		with GlobalDB() as value:
			await dump_respond(("global", value), ctx=ctx, ephemeral=ephemeral, to_file=to_file)
