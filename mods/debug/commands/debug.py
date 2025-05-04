from common.bot import MCL
from dev.commands._base import GROUP_DEV
from miru.ext import menu
from prelude import *


class MainScreen(menu.Screen):
	# This method must be overridden in your screen classes
	# This is where you would fetch data from a database, etc. to display on your screen
	async def build_content(self) -> menu.ScreenContent:
		return menu.ScreenContent(
			embed=hikari.Embed(
				title="Welcome to the Miru Menu example!",
				description="This is an example of the Miru Menu extension.",
				color=0x00FF00,
			)
		)

	# Note: You should always use @menu decorators inside Screen subclasses, NOT @miru
	@menu.button(label="Moderation")
	async def moderation(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		# Add a new screen to the menu stack, the message is updated automatically
		await self.menu.push(ModerationScreen(self.menu))

	@menu.button(label="Logging")
	async def logging(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		await self.menu.push(LoggingScreen(self.menu))


class ModerationScreen(menu.Screen):
	async def build_content(self) -> menu.ScreenContent:
		return menu.ScreenContent(embed=hikari.Embed(title="Moderation", description="This is the moderation screen!", color=0x00FF00))

	@menu.button(label="Back")
	async def back(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		# Remove the current screen from the menu stack,
		# effectively going back to the previous screen
		await self.menu.pop()

	@menu.button(label="Ban", style=hikari.ButtonStyle.DANGER)
	async def ban(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		await ctx.respond("Hammer time!")

	@menu.button(label="Kick", style=hikari.ButtonStyle.SECONDARY)
	async def kick(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		await ctx.respond("Kick!")


class LoggingScreen(menu.Screen):
	def __init__(self, menu: menu.Menu) -> None:
		super().__init__(menu)
		# Your screens can store state in the class instance
		# But keep in mind that the instance will be
		# destroyed once the screen is popped off the stack
		self.is_enabled = False

	async def build_content(self) -> menu.ScreenContent:
		return menu.ScreenContent(embed=hikari.Embed(title="Logging", description="This is the logging screen!", color=0x00FF00))

	@menu.button(label="Back")
	async def back(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		await self.menu.pop()

	@menu.button(label="Enable", style=hikari.ButtonStyle.DANGER)
	async def enable(self, ctx: miru.ViewContext, button: menu.ScreenButton) -> None:
		self.is_enabled = not self.is_enabled
		button.style = hikari.ButtonStyle.SUCCESS if self.is_enabled else hikari.ButtonStyle.DANGER
		button.label = "Disable" if self.is_enabled else "Enable"
		# Update the message the menu is attached to with the new state of components.
		await self.menu.update_message()


@GROUP_DEV.include
@arc.slash_subcommand("debug", "Debug random stuff...")
async def cmd_dev_debug(ctx: arc.GatewayContext) -> None:
	my_menu = menu.Menu(timeout=3)

	builder = await my_menu.build_response_async(MCL, MainScreen(my_menu))
	await ctx.respond_with_builder(builder)
	MCL.start_view(my_menu)
