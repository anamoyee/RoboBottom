from collections.abc import Callable
from itertools import groupby

import arc
import hikari
import miru
from arc.client import GatewayContext
from miru.ext import menu

from prelude import RbBM, c, pd

from ..config import S
from ..db import Profile, UserDB


class _BaseSetting(RbBM):
	emoji: str
	name: str
	display_name: str
	description: str

	def Screen(self, cmd_ctx: arc.GatewayContext) -> type[menu.Screen]:
		raise NotImplementedError("Subclasses must implement this method")

	def get_from_profile(self, prof: Profile) -> str:
		raise NotImplementedError("Subclasses must implement this method")
		# return prof.settings.__getitem__(self.name)

	def set_in_profile(self, prof: Profile, str_value: str) -> None:
		raise NotImplementedError("Subclasses must implement this method")
		# prof.settings.__setitem__(self.name, value)


class _BaseSelectSetting(_BaseSetting):
	options: list[miru.SelectOption] | None
	placeholder: str = "Select option"

	def Screen(self, cmd_ctx: arc.GatewayContext) -> type[menu.Screen]:
		class _BaseSelectSettingScreen(menu.Screen):
			async def build_content(self2) -> menu.ScreenContent:  # noqa: N805
				with UserDB(cmd_ctx.author.id) as user:
					prof = await user.ensure_profile(cmd_ctx)

					current_value = self.get_from_profile(prof)

				return menu.ScreenContent(
					embed=hikari.Embed(
						title=f"{self.emoji} {self.display_name}",
						description=f"""
{self.description}
> Currently **{current_value}**
"""[1:-1],
						color=S.COLOR.PRIMARY,
					),
				)

			@menu.text_select(options=self.options, placeholder=self.placeholder, row=0)
			async def on_select(self2, ctx: miru.ViewContext, slm: miru.TextSelect) -> None:  # noqa: N805
				if ctx.author.id != cmd_ctx.author.id:
					await ctx.respond("not your menu", flags=hikari.MessageFlag.EPHEMERAL)  # TODO: make "<megu pressing button image>" and simillar async def(ctx)

				val = slm.values[0]

				with UserDB(cmd_ctx.author.id) as user:
					prof = await user.ensure_profile(cmd_ctx)

					self.set_in_profile(prof, val)

				await self2.menu._load_screen(self2.menu.current_screen)
				await self2.menu.update_message()  # discard the expected response & update the message with new value

		return _BaseSelectSettingScreen

	@pd.field_validator("options", mode="before")
	@classmethod
	def validate_options_length(cls, value: list[miru.SelectOption] | None) -> list[miru.SelectOption] | None:
		if value is None:
			return value

		if not (24 >= len(value) >= 1):
			raise ValueError("At least one and at most 24 option(s) required")

		return list(value)


# class _BaseModalSetting(_BaseSetting):
# 	...


class PrivateSetting(_BaseSelectSetting):
	emoji: str = "🌐"
	name: str = "visibility"
	display_name: str = "Visibility"
	description: str = "If other members can view your animal list"

	options: list[miru.SelectOption] = (
		miru.SelectOption(label="Public", value="public", emoji="🌎"),
		miru.SelectOption(label="Private", value="private", emoji="🔒"),
	)

	def get_from_profile(self, prof: Profile) -> str:
		return {True: "private", False: "public"}[prof.settings.private]

	def set_in_profile(self, prof: Profile, str_value: str) -> None:
		prof.settings.private = {"private": True, "public": False}[str_value]


SETTINGS = [
	# Setting(
	# 	emoji="🏷",
	# 	name="name",
	# 	display_name="Profile Name",
	# 	description="The name of your profile",
	# 	options=None,
	# ),
	PrivateSetting(),
]


class SettingsMainScreen(menu.Screen):
	cmd_ctx: arc.GatewayContext

	def __init__(self, menu: menu.Menu, cmd_ctx: arc.GatewayContext) -> None:
		self.cmd_ctx = cmd_ctx

		super().__init__(menu)

	async def build_content(self) -> menu.ScreenContent:
		author: hikari.User = self.cmd_ctx.author

		with UserDB(author.id) as user:
			prof = await user.ensure_profile(self.cmd_ctx)

		return menu.ScreenContent(
			embed=hikari.Embed(
				title=None,
				description="\n".join(f"{s.emoji} {s.display_name}: {s.get_from_profile(prof)}" for s in SETTINGS),
				color=S.COLOR.PRIMARY,
			).set_author(name="Profile Settings", icon=author.avatar_url),
		)

	@menu.text_select(options=[miru.SelectOption(label=s.display_name, value=s.name, emoji=s.emoji) for s in SETTINGS], row=0, placeholder="Select option")
	async def on_select(self, ctx: miru.ViewContext, slm: miru.TextSelect) -> None:
		value = slm.values[0]

		setting = next(x for x in SETTINGS if x.name == value)

		with UserDB(self.cmd_ctx.author.id) as user:
			await user.ensure_profile(self.cmd_ctx)

		await self.menu.push(setting.Screen(self.cmd_ctx)(self.menu))
