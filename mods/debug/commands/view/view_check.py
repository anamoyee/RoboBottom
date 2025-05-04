from miru import ViewContext as _ViewContext

from . import _base


class ClearComponents(_base.MustHaveMessageView, _base.ClearComponentsMethodView):
	"""Edit view's bound message's `components=[]` when any input is received."""

	async def view_check(self, ctx: _ViewContext) -> bool:
		await self.clear_components_and_edit()

		return await super().view_check(ctx)


class DisableComponents(_base.MustHaveMessageView, _base.DisableComponentsMethodView):
	"""Disable view's bound message's components when any input is received."""

	async def view_check(self, ctx: _ViewContext) -> bool:
		await self.disable_components_and_edit()

		return await super().view_check(ctx)
