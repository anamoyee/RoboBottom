from common.bot import MCL
from dev.commands._base import GROUP_DEV
from miru.ext import nav
from prelude import *


class MyNavButton(nav.NavButton):
	async def callback(self, context: miru.ViewContext) -> None:
		await context.respond("You clicked me!", flags=hikari.MessageFlag.EPHEMERAL)

	async def before_page_change(self) -> None:
		self.label = f"Page: {self.view.current_page + 1}"


class MyNavSelect(nav.NavTextSelect):
	async def callback(self, context: miru.ViewContext) -> None:
		await context.respond(f"You selected {self.values[0]}", flags=hikari.MessageFlag.EPHEMERAL)


@GROUP_DEV.include
@arc.slash_subcommand("debug2", "Debug more random stuff...")
async def cmd_dev_debug2(ctx: arc.GatewayContext) -> None:
	embed = hikari.Embed(title="I'm the second page!", description="Also an embed!")
	page = nav.Page(content="I'm the last page!", embed=hikari.Embed(title="I also have an embed!"))
	pages = ["I'm the first page!", embed, page]

	items = [
		nav.PrevButton(),
		nav.StopButton(),
		nav.NextButton(),
		MyNavButton(label="Page: 1", row=1),
		MyNavSelect(
			options=[miru.SelectOption(x, x) for x in ("option 1", "option 2", "option 3")],
			row=2,
		),
	]

	navigator = nav.NavigatorView(pages=pages, items=items)

	builder = await navigator.build_response_async(MCL)
	await ctx.respond_with_builder(builder)
	MCL.start_view(navigator)
