from r04_bot import *


# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
class EMBED:
  @staticmethod
  def generic_error(e: Exception, *, color=S.EMBED_COLORS['error'], **kwargs) -> hikari.Embed:
    return embed(
      *tcr.extract_error(e, raw=True),
      color=color,
      **kwargs,
    )

  @staticmethod
  def generic_text_error(title: str = 'An error occured', description: str = 'No further information provided', *, color=S.EMBED_COLORS['error'], **kwargs) -> hikari.Embed:
    return embed(
      title,
      description,
      color=color,
      **kwargs,
    )

  @staticmethod
  def reminder(reminder: Reminder) -> hikari.Embed:
    override_kwargs = {}
    if (expired_for := reminder.expired_for()) > S.APOLOGISE_FOR_INCONVENIENCE_AFTER_EXPIRED_FOR:
      override_kwargs['footer'] = S.REMINDER_EXPIRED_FOOTER.replace('{expired_for}', TIMESTR.to_str(expired_for))

    return embed(
      description=reminder.text,
      **{**S.REMINDER_EMBED, **override_kwargs},
    )

  @staticmethod
  def reminder_list(rems: t.Iterable[tuple[int, Reminder]], total_reminders: int, **kwargs) -> hikari.Embed:
    desc = '\n'.join(f'{i}) {rem!s}' for i, rem in rems)

    cancelrange = f'1-{total_reminders}' if total_reminders else 'idx'

    desc += f'\n\nCancel a reminder with `cancel <{cancelrange}>`'
    desc = desc.strip()

    settings_kwargs = S.REMINDER_LIST_EMBED.copy()
    settings_kwargs['title'] = settings_kwargs['title'].replace('{amount}', str(total_reminders))

    return embed(description=desc, **{**settings_kwargs, **kwargs})

  @staticmethod
  def reminder_canceled(rem: Reminder) -> hikari.Embed:
    if rem.is_flag(CTF.HASH_HIDDEN):
      desc = "`>> This reminder was hidden <<`\nIts contents were irrecoverably lost!"
    else:
      desc = str(rem)

    return embed(
      '🔕 Reminder cancelled!',
      desc,
      color=S.EMBED_COLORS['cancelled'],
    )

  @staticmethod
  def reminder_view(rem: Reminder) -> hikari.Embed:
    if rem.is_flag(CTF.HASH_HIDDEN):
      desc = "`>> This reminder is hidden <<`\nIts contents will only be shown when it's triggered (not cancelled)"
    else:
      desc = rem.text

    return embed(
      f'📝 {"Hidden " if rem.is_flag(CTF.HASH_HIDDEN) else ""}Reminder #{rem.fetch_index()+1}',
      description=desc,
      footer=f'Will trigger in {TIMESTR.to_str(-rem.expired_for())} ({TIMESTR.to_datestr(-rem.expired_for())})',
      color=S.EMBED_COLORS['secondary'],
    )

  @staticmethod
  def user_settings_single(key: str, value: Any) -> hikari.Embed:
    return embed(
      f'User settings: {key.title()}',
      f'Currently set to: **`{value}`** ',
      color=S.EMBED_COLORS['settings'],
    )

  @staticmethod
  def setting_changed(key: str, value: str) -> hikari.Embed:
    return embed(
      f'Setting changed: {key.title()}',
      f'Changed to: **`{value}`**',
      color=S.EMBED_COLORS['settings'],
    )

  @staticmethod
  def settings_invalid_characters() -> hikari.Embed:
    return embed(
      'Invalid setting value.',
      'Only the following characters are allowed: `a-z`, `A-Z`, `0-9`, `_- `\nSetting value cannot be empty.',
      color=S.EMBED_COLORS['error'],
    )

  @staticmethod
  def settings_value_too_long() -> hikari.Embed:
    return embed(
      'Invalid setting value.',
      f'Setting value cannot be longer than {SETTINGS_VALUE_MAX_LENGTH} characters.',
      color=S.EMBED_COLORS['error'],
    )


class RESP:
  @staticmethod
  async def must_use_dms(user_id: int, **kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> tcr.discord.types.HikariDictMessage:
    channel = await BOT.rest.create_dm_channel(user_id)
    return {
      'content': f':x: This command cannot be used outside of [DMs](<https://discord.com/channels/@me/{channel.id}>).',
      'flags': hikari.MessageFlag.EPHEMERAL,
      **kwargs,
    }

  @staticmethod
  def not_dev(**kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> tcr.discord.types.HikariDictMessage:
    return {
      'content': ':x: You are not allowed to use this command.',
      'flags': hikari.MessageFlag.EPHEMERAL,
      **kwargs,
    }

  @staticmethod
  def reminder_list(r: t.Iterable[Reminder], **kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> nav.NavigatorView:
    """List of user's reminders.

    After that:
    ```py
    builder = await navigator.build_response_async(ACL)
    await builder.send_to_channel(channel_id)
    ACL.start_view(navigator)
    ```
    """
    pages = []

    for remslice in tcr.batched(list(enumerate(r, start=1)), S.REMINDER_LIST_REMINDERS_PER_PAGE) or [[]]:
      pages.append(nav.Page(embed=EMBED.reminder_list(remslice, len(r))))

    return nav.NavigatorView(pages=pages, items=[x() for x in (S.REMINDER_LIST_NAVBAR_ITEMS if len(pages) > 1 else S.REMINDER_LIST_NAVBAR_ITEMS_ONE_PAGE)], **kwargs)
