import io
import zipfile

import arc
import hikari
from tcrutils.codeblock import codeblocks
from tcrutils.print import fmt_iterable

from ..config import S
from .ephemeral import ephemeral_from_bool


async def dump_respond(
	*name_obj_tuples: tuple[str, object],
	ctx: arc.GatewayContext,
	ephemeral: bool,
	to_file: bool,
) -> None:
	name_obj_tuples = [(str(name), obj) for (name, obj) in name_obj_tuples]

	if to_file:
		await dump_respond_file(*name_obj_tuples, ctx=ctx, ephemeral=ephemeral)
	else:
		await dump_respond_to_codeblock(*name_obj_tuples, ctx=ctx, ephemeral=ephemeral)


async def dump_respond_to_codeblock(
	*name_obj_tuples: tuple[str, object],
	ctx: arc.GatewayContext,
	ephemeral: bool,
	langcode: str = "py",
) -> None:
	flags = ephemeral_from_bool(ephemeral)

	if not name_obj_tuples:
		await ctx.respond(f"{S.NO} Nobody here but us chickens!", flags=flags)
		return

	should_add_count = len(name_obj_tuples) > 1

	content = codeblocks(
		*(f"# {name!r}\n" + fmt_iterable(obj) for (name, obj) in name_obj_tuples),
		*((f"Dumped {len(name_obj_tuples)} records",) if should_add_count else ()),
		langcodes=[langcode] * len(name_obj_tuples) + ([""] if should_add_count else []),
	)

	await ctx.respond(content, flags=flags)


async def dump_respond_file(
	*name_obj_tuples: tuple[str, object],
	ctx: arc.GatewayContext,
	ephemeral: bool,
	ext: str = ".py",
	spoiler: bool = False,
) -> None:
	flags = ephemeral_from_bool(ephemeral)

	if not name_obj_tuples:
		await ctx.respond(f"{S.NO} Nobody here but us chickens!", flags=flags)
		return

	content = f"Dumped {records_n} records" if (records_n := len(name_obj_tuples)) > 1 else ""

	if len(name_obj_tuples) <= 10:
		await ctx.respond(
			content,
			attachments=[
				hikari.files.Bytes(
					fmt_iterable(obj).encode("utf-8"),
					f"{name}{ext}",
					spoiler=spoiler,
				)
				for (name, obj) in name_obj_tuples
			],
			flags=flags,
		)

	else:
		# Creating an in-memory ZIP file if >10 attachments are needed
		content += "\nSince you have more than 10 objects to dump, I will send them as a zip file instead."

		zip_buffer = io.BytesIO()
		with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
			for name, obj in name_obj_tuples:
				file_data = fmt_iterable(obj).encode("utf-8")
				zip_file.writestr(f"{name}{ext}", file_data)

		zip_buffer.seek(0)

		await ctx.respond(
			content or hikari.UNDEFINED,
			attachments=[hikari.files.Bytes(zip_buffer.getvalue(), "dump.zip", spoiler=spoiler)],
			flags=flags,
		)
