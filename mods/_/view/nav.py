from collections.abc import Callable, Sequence
from datetime import timedelta

import hikari
import miru
from arc import GatewayContext
from miru.ext import nav
from tcrutils.iterable import batched


class NavigatorViewArcHelper(nav.NavigatorView):
	async def respnd_via_context(self, *, ctx: GatewayContext, mcl: miru.Client):
		builder = await self.build_response_async(mcl)
		try:
			return await ctx.respond_with_builder(builder)
		finally:
			if self.children:  # <-- prevent: "WARN: miru.view: View 'LinesPagedView' has no items attached. Ignoring 'Client.start_view()' call"
				mcl.start_view(self)


class PrevButton(nav.PrevButton):
	def __init__(self, *, row: int = 0, position: int = 0):
		super().__init__(
			style=hikari.ButtonStyle.SUCCESS,
			label="<< Page %d",
			emoji=None,
			row=row,
			position=position,
		)

	def before_page_change(self):
		self.label = f"<< Page {self.view.current_page}"

		return super().before_page_change()  # ensure disabled if no more prev pages


class NextButton(nav.NextButton):
	def __init__(self, *, row: int = 0, position: int = 1):
		super().__init__(
			style=hikari.ButtonStyle.SUCCESS,
			label="Page %d >>",
			emoji=None,
			row=row,
			position=position,
		)

	def before_page_change(self):
		self.label = f"Page {self.view.current_page + 2} >>"

		return super().before_page_change()  # ensure disabled if no more next pages


class PagedView(NavigatorViewArcHelper, nav.NavigatorView):
	"""Standard paginator, any items are extra, this means the list already includes two buttons for pagination at row 0, positions 0 and 1. This does not support the zoo sorting."""

	def __init__(
		self,
		*,
		pages: Sequence[str | hikari.Embed | Sequence[hikari.Embed] | nav.Page],
		extra_items: Sequence[nav.NavItem] = (),
		timeout: float | int | timedelta | None = None,
		autodefer: bool | miru.AutodeferOptions = True,
	) -> None:
		super().__init__(
			pages=pages,
			items=(
				*(
					(
						PrevButton(),
						NextButton(),
					)
					if len(pages) > 1
					else ()
				),
				*extra_items,
			),
			timeout=timeout,
			autodefer=autodefer,
		)


class LinesPagedView(PagedView):
	def __init__(
		self,
		lines: Sequence[str],
		*,
		n: int,
		embed_from_description_fn: Callable[[str, int, int], hikari.Embed],
		extra_items: Sequence[nav.NavItem] = (),
		timeout: float | int | timedelta | None = None,
		autodefer: bool | miru.AutodeferOptions = True,
	):
		"""Put lines of text into zoo-styled pages of n lines each (think: /animals command).

		Args:
			lines: The lines of text to put into pages.
			n: The number of lines per page.
			embed_from_description_builder_fn: A function that takes embed_description, i, ii: str and returns an Embed instance, where embed_description is.. (self explainatory), i is the current page number (0-indexed), ii is len(pages). This is called once for every page.
		"""

		batches = batched(lines, n=n)
		ii = len(batches)

		super().__init__(
			pages=[embed_from_description_fn("\n".join(batch), i, ii) for i, batch in enumerate(batches)],
			extra_items=extra_items,
			timeout=timeout,
			autodefer=autodefer,
		)
