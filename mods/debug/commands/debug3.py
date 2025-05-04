from collections.abc import Sequence
from datetime import timedelta

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


class ThreeDNavigatorViewLayer:
	def __init__(self, pages: Sequence[nav.Page], items: Sequence[nav.NavItem], label: str):
		self.pages = pages
		self.items = items
		self.label = label

	def modify_buttton(self, button: "ThreeDNavigatorViewLayerButton") -> None:
		button.label = self.label


class ThreeDNavigatorViewLayerButton(nav.NavButton):
	view: "ThreeDNavigatorView"

	def __init__(
		self,
		label: str | None = None,
		*,
		emoji: hikari.Emoji | str | None = None,
		style: hikari.ButtonStyle = hikari.ButtonStyle.PRIMARY,
		row: int = 0,
		position: int = 4,
	):
		super().__init__(label, emoji=emoji, style=style, disabled=False, row=row, position=position)

	async def callback(self, ctx: miru.ViewContext) -> None:
		self.view.next_layer()
		await self.view.send_page(ctx)


class ThreeDNavigatorView(nav.NavigatorView):
	def next_layer(self):
		self.layers.append(self.layers.pop(0))
		self._pages = self.layers[0].pages
		self.current_page = 0

		self.clear_items()

		if len(self.layers) >= 2:
			self.layers[1].modify_buttton(self.next_button)
			self.add_item(self.next_button)

		for item in self.layers[0].items:
			self.add_item(item)

	def __init__(
		self,
		layer0: ThreeDNavigatorViewLayer,
		*layers: ThreeDNavigatorViewLayer,
		timeout: float | int | timedelta | None = None,
		autodefer: bool | miru.AutodeferOptions = True,
	):
		self.layers = [layer0, *layers]
		if len(self.layers) == 1:
			super().__init__(pages=layer0.pages, items=layer0.items, timeout=timeout, autodefer=autodefer)
		elif len(self.layers) >= 2:
			self.next_button = ThreeDNavigatorViewLayerButton("")
			self.layers[1].modify_buttton(self.next_button)
			super().__init__(pages=layer0.pages, items=(layer0.items + [self.next_button]), timeout=timeout, autodefer=autodefer)


@GROUP_DEV.include
@arc.slash_subcommand("debug3", "Debug more random stuff...")
async def cmd_dev_debug3(ctx: arc.GatewayContext) -> None:
	embed = hikari.Embed(title="I'm the second page!", description="Also an embed!")
	page = nav.Page(content="I'm the last page!", embed=hikari.Embed(title="I also have an embed!"))
	pages1 = [nav.Page(content="I'm the first page!"), nav.Page(embed=embed), page]

	items1 = [
		nav.PrevButton(row=0, position=0),
		nav.StopButton(row=0, position=1),
		nav.NextButton(row=0, position=2),
		MyNavButton(label="Page: 1", row=1, position=0),
		MyNavSelect(
			options=[miru.SelectOption(x, x) for x in ("option 1", "option 2", "option 3")],
			row=2,
		),
	]

	pages2 = [
		nav.Page(content="p1"),
		nav.Page(content="p2"),
		nav.Page(content="p3"),
	]

	items2 = [
		nav.PrevButton(row=0, position=0),
		nav.IndicatorButton(row=0, position=1),
		nav.NextButton(row=0, position=2),
	]

	navigator = ThreeDNavigatorView(
		ThreeDNavigatorViewLayer(pages=pages1, items=items1, label="First Layer"),
		ThreeDNavigatorViewLayer(pages=pages2, items=items2, label="Second Layer"),
	)

	builder = await navigator.build_response_async(MCL)
	await ctx.respond_with_builder(builder)
	MCL.start_view(navigator)
