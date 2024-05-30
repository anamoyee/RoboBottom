from r09_validate import *

if True:  # Global Components

  class DefaultLabelNavButton(nav.NavButton):
    def __init__(self, *, label: str | None = None, **kwargs):
      super().__init__(label=label or '.', **kwargs)

  class PrevNavButton(DefaultLabelNavButton):
    async def callback(self, context: miru.ViewContext) -> None:
      self.view.current_page -= 1
      await self.view.send_page(context)

    async def before_page_change(self) -> None:
      self.disabled = self.view.current_page <= 0
      self.style = hikari.ButtonStyle.DANGER if self.disabled else hikari.ButtonStyle.SUCCESS
      self.label = S.NAVBAR_LABEL['prev'].replace('{page}', str(self.view.current_page))

  class NextNavButton(DefaultLabelNavButton):
    async def callback(self, context: miru.ViewContext) -> None:
      self.view.current_page += 1
      await self.view.send_page(context)

    async def before_page_change(self) -> None:
      self.disabled = self.view.current_page >= len(self.view.pages) - 1
      self.style = hikari.ButtonStyle.DANGER if self.disabled else hikari.ButtonStyle.SUCCESS
      self.label = S.NAVBAR_LABEL['next'].replace('{page}', str(self.view.current_page + 2))


if True:  # Settings

  class ChangeSettingNavButton(nav.NavButton):
    def __init__(
      self,
      label: str | None = None,
      *,
      emoji: Emoji | str | None = None,
      style: Literal[ButtonStyle.PRIMARY, ButtonStyle.SECONDARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER] = hikari.ButtonStyle.PRIMARY,
      disabled: bool = False,
      custom_id: str | None = None,
      row: int | None = None,
      position: int | None = None,
      autodefer: bool | AutodeferOptions | UndefinedType = hikari.UNDEFINED,
    ) -> None:
      super().__init__(label or '.', emoji=emoji, style=style, disabled=disabled, custom_id=custom_id, row=row, position=position, autodefer=autodefer)

    async def before_page_change(self) -> None:
      self.label = SETTINGS_LABEL_LOOKUP.get(SETTINGS_PAGE_KEYS[self.view.current_page], SETTINGS_LABEL_LOOKUP[None])

    async def callback(self, ctx: miru.ViewContext):
      async def mcb(mod: miru.Modal, ctx: miru.ModalContext, values: list[str]) -> None:
        udb = Database(ctx.author.id)
        us = udb['s']

        if (not values[0]) or (not all(x in SETTINGS_VALUE_ALLOWED_CHARACTERS for x in values[0])):
          await ctx.respond(EMBED.settings_invalid_characters(), flags=hikari.MessageFlag.EPHEMERAL)
          return

        if len(values[0]) > SETTINGS_VALUE_MAX_LENGTH:
          await ctx.respond(EMBED.settings_value_too_long(), flags=hikari.MessageFlag.EPHEMERAL)
          return

        setattr(us, SETTINGS_PAGE_KEYS[self.view.current_page], values[0])
        udb['s'] = us

        self.view.pages[self.view.current_page] = EMBED.user_settings_single(SETTINGS_PAGE_KEYS[self.view.current_page], values[0])
        await self.view.message.edit(self.view.pages[self.view.current_page])
        await ctx.respond(EMBED.setting_changed(SETTINGS_PAGE_KEYS[self.view.current_page], values[0]), flags=hikari.MessageFlag.EPHEMERAL)

      await modal(
        ctx.respond_with_modal,
        mcb,
        miru.TextInput(label='New value for the setting', max_length=100, min_length=1, required=True),
        title=f'Set {(SETTINGS_PAGE_KEYS[self.view.current_page]).title()!r}',
      )

  class SettingsPrevNavButton(nav.PrevButton):
    def __init__(
      self,
      *,
      style: Literal[ButtonStyle.PRIMARY, ButtonStyle.SECONDARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER] = hikari.ButtonStyle.PRIMARY,
      label: str | None = None,
      custom_id: str | None = None,
      emoji: Emoji | str | None = None,
      row: int | None = None,
      position: int | None = None,
    ):
      super().__init__(style=style, label=label or '.', custom_id=custom_id, emoji=emoji, row=row, position=position)

    async def before_page_change(self) -> None:
      self.disabled = self.view.current_page == 0
      self.style = hikari.ButtonStyle.DANGER if self.disabled else hikari.ButtonStyle.SUCCESS
      self.label = S.NAVBAR_LABEL['prev'].replace('{page}', str(self.view.current_page))

  class SettingsNextNavButton(nav.NextButton):
    def __init__(
      self,
      *,
      style: Literal[ButtonStyle.PRIMARY, ButtonStyle.SECONDARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER] = hikari.ButtonStyle.PRIMARY,
      label: str | None = None,
      custom_id: str | None = None,
      emoji: Emoji | str | None = None,
      row: int | None = None,
      position: int | None = None,
    ):
      super().__init__(style=style, label=label or '.', custom_id=custom_id, emoji=emoji, row=row, position=position)

    async def before_page_change(self) -> None:
      self.disabled = self.view.current_page >= len(self.view.pages) - 1
      self.style = hikari.ButtonStyle.DANGER if self.disabled else hikari.ButtonStyle.SUCCESS
      self.label = S.NAVBAR_LABEL['next'].replace('{page}', str(self.view.current_page + 2))


S.SETTINGS_NAVBAR_ITEMS = [
  SettingsPrevNavButton,
  partial(nav.IndicatorButton, style=hikari.ButtonStyle.SUCCESS),
  SettingsNextNavButton,
  ChangeSettingNavButton,
]

S.REMINDER_LIST_NAVBAR_ITEMS = [
  PrevNavButton,
  NextNavButton,
]

S.REMINDER_LIST_NAVBAR_ITEMS_ONE_PAGE = []
