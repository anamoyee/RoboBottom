from . import _base


class ClearComponents(_base.MustHaveMessageView, _base.ClearComponentsMethodView):
	"""Edit view's bound message's `components=[]` when view times out."""

	async def on_timeout(self) -> None:
		await self.clear_components_and_edit()

		await super().on_timeout()


class DisableComponents(_base.MustHaveMessageView, _base.DisableComponentsMethodView):
	"""Disable view's bound message's components when view times out."""

	async def on_timeout(self) -> None:
		await self.disable_components_and_edit()

		await super().on_timeout()
