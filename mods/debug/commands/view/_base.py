from collections.abc import Awaitable, Callable, Iterable

import hikari
import miru
from miru.abc.item import ViewItem as _ViewItem
from tcrutils.void import alambda as _alambda


async def clear_components_and_edit(message: hikari.Message):
	"""Edit this message to contain no components (`components=[]`)."""
	await message.edit(components=[])


async def disable_components_and_edit(message: hikari.Message, *, stay_predicate: Callable[[hikari.Message, int, _ViewItem], Awaitable[bool]] = _alambda(lambda m, i, vi: True)):
	"""Edit this message such that all components on it will be disabled=True, if stay_predicate."""
	new_view = miru.View().from_message(message)

	components = list(new_view.children)

	for i, component in enumerate(components):
		if hasattr(component, "disabled"):
			component.disabled = True

		if not await stay_predicate(message, i, component):
			new_view.remove_item(component)

	await message.edit(components=new_view)
	# No need to start view since all components are disabled.


class ClearComponentsMethodView(miru.View):
	async def clear_components_and_edit(self):
		await clear_components_and_edit(self.message)


class DisableComponentsMethodView(miru.View):
	async def disable_components_and_edit(self, *, stay_predicate: Callable[[hikari.Message, int, _ViewItem], Awaitable[bool]] = _alambda(lambda m, i, vi: True)):
		await disable_components_and_edit(self.message, stay_predicate=stay_predicate)


class MustHaveMessageView(miru.View):
	"""Subclass to assert existence of a valid self.message (not self._message_id nor self.is_bound)."""

	def _client_start_hook(self, *args, **kwargs) -> None:
		if self.message is None:
			if self._message_id is not None:
				raise RuntimeError(f"{self.__class__.__name__} is required to be bound to a message (!!! NOT MESSAGE ID !!!) when starting, like this: miru_client.start_view(view, message_id=message.id)")
			raise RuntimeError(f"{self.__class__.__name__} is required to be bound to a message when starting, like this: miru_client.start_view(view, bind_to=message)")

		return super()._client_start_hook(*args, **kwargs)
