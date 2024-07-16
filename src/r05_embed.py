import r07_syncs as m_syncs
import r10_components as m_components
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
  def reminder(rem: Reminder) -> hikari.Embed:
    override_kwargs = {}
    if (expired_for := rem.expired_for(not_counting_timeout=True)) > S.APOLOGISE_FOR_INCONVENIENCE_AFTER_EXPIRED_FOR:
      if rem.timeout:
        override_kwargs[
          'footer'
        ] = f"This reminder was sent {{expired_for}} too late because I wasn't able to reach you! (Have you blocked me?? :c). If you didnt block the bot, contact me, the developer: {S.CREATED_BY_STR!s}"
      else:
        override_kwargs['footer'] = S.REMINDER_EXPIRED_FOOTER
      override_kwargs['footer'] = override_kwargs['footer'].replace('{expired_for}', TIMESTR.to_str(expired_for))

    desc = rem.text

    if not desc:
      desc = m_syncs.somehow_you_managed_to('have an empty reminder (with no text)')

    return embed(
      description=desc,
      **{**S.REMINDER_EMBED, **override_kwargs},
    )

  @staticmethod
  def reminder_safemode() -> hikari.Embed:
    return embed(
      'Internal error',
      'Oops there was an issue sending your reminder, you can see the unprocessed and raw reminders in the text attachments below.',
      color=S.EMBED_COLORS['error'],
    )

  @staticmethod
  def reminder_list(rems: t.Iterable[tuple[int, Reminder]], total_reminders: int, archive: bool = False, **kwargs) -> hikari.Embed:
    desc = '\n'.join(f'{i}) {rem!s}' for i, rem in rems)

    cancelrange = f'1-{total_reminders}' if total_reminders else 'idx'

    if not archive:
      desc += f'\n\nCancel a reminder with `cancel <{cancelrange}>`'
    elif not desc:
      desc = 'You have no reminders in your archive.'
    desc = desc.strip()

    settings_kwargs = S.REMINDER_LIST_EMBED.copy()
    settings_kwargs['title'] = settings_kwargs['title'].replace('{amount}', str(total_reminders))
    if archive:
      settings_kwargs['color'] = S.EMBED_COLORS['archive']
      settings_kwargs['title'] = settings_kwargs['title'] + '- Archive'

    if any(rem.timeout for _, rem in rems):
      kwargs['footer'] = f"""
At least 1 of your reminders is timed out.
This means I wasn't able to deliver it to you when it expired (for example you blocked the bot), since you're seeing this, there seems to be an issue with my code, please contact me and report this bug:
{S.CREATED_BY_STR})
"""[1:-1]

    return embed(description=desc, **{**settings_kwargs, **kwargs})

  @staticmethod
  def reminder_canceled(rem: Reminder, *, archive: bool = False) -> hikari.Embed:
    if not archive and rem.is_flag(CTF.HASH_HIDDEN):
      desc = '`>> This reminder was hidden <<`\nIts contents were irrecoverably lost!'
    else:
      desc = rem.text

    if not desc:
      desc = m_syncs.somehow_you_managed_to('have an empty reminder (with no text)')

    return embed(
      '🔕 Reminder cancelled!' if not archive else '🔕 Reminder removed from archive!',
      desc,
      color=S.EMBED_COLORS['cancelled'] if not archive else S.EMBED_COLORS['archive'],
    )

  @staticmethod
  def reminder_view(rem: Reminder, rem_index: int, *, archive: bool = False) -> hikari.Embed:
    if not archive and rem.is_flag(CTF.HASH_HIDDEN):
      desc = "`>> This reminder is hidden <<`\nIts contents will only be shown when it's triggered (not cancelled)"
    else:
      desc = rem.text

    if not desc:
      desc = m_syncs.somehow_you_managed_to('have an empty reminder (with no text)')

    footer = f'{"Will trigger" if not archive else "Was scheduled to trigger"} in {TIMESTR.to_str(-rem.expired_for())} ({TIMESTR.to_strf(-rem.expired_for())})'
    if rem.attachments:
      footer += f' + {rem.attachments_as_listabbrev().strip()}'

    return embed(
      f'📝 {"Hidden " if not archive and rem.is_flag(CTF.HASH_HIDDEN) else ""}{"Archived " if archive else ""}Reminder #{rem_index+1}',
      description=desc,
      footer=footer,
      color=S.EMBED_COLORS['secondary'] if not archive else S.EMBED_COLORS['archive'],
    )

  @staticmethod
  def import_confirmer(import_obj: ExportedDataTD, mode: Literal['append', 'overwrite'], invalid_keys: list[str]) -> hikari.Embed:
    desc = 'This will:'

    def sortkey(key: str):
      if key == 'reminders':
        return ''
      return key

    keys = sorted(import_obj.keys(), key=sortkey)

    for key in keys:
      if key == 'reminders':
        desc += f'\n- **{mode.upper()}** reminders (any expired reminders will be skipped)'
      else:
        desc += f'\n- **OVERWRITE** {key}'

    if invalid_keys:
      invalid_keys_formatted = ', '.join(f'`{k}`' for k in invalid_keys)

    color = S.EMBED_COLORS['success']

    if '\n' not in desc:
      color = S.EMBED_COLORS['error']
      desc = (
        'This file doesnt seem to contain any valid changes to the database (confirming will do nothing). Please check the file integrity and contact the bot developer in case of any issues.'
      )
      if invalid_keys:
        desc += f'\n\nThis issue might be due to the file containing invalid keys:\n{invalid_keys_formatted}'
    elif invalid_keys:
      color = S.EMBED_COLORS['colon']  # orange halfway between success and error i guess?
      desc += f'\nThere were also invalid keys in the file: {invalid_keys_formatted}'

    return embed(
      'Are you sure you want to import this file?',
      desc,
      color=color,
    )

  # @staticmethod
  # def user_settings_single(key: str, value: Any) -> hikari.Embed:
  #   return embed(
  #     f'User settings: {key.title()}',
  #     f'Currently set to: **`{value}`** ',
  #     color=S.EMBED_COLORS['settings'],
  #   )

  # @staticmethod
  # def setting_changed(key: str, value: str) -> hikari.Embed:
  #   return embed(
  #     f'Setting changed: {key.title()}',
  #     f'Changed to: **`{value}`**',
  #     color=S.EMBED_COLORS['settings'],
  #   )

  # @staticmethod
  # def settings_invalid_characters() -> hikari.Embed:
  #   return embed(
  #     'Invalid setting value.',
  #     'Only the following characters are allowed: `a-z`, `A-Z`, `0-9`, `_- `\nSetting value cannot be empty.',
  #     color=S.EMBED_COLORS['error'],
  #   )

  # @staticmethod
  # def settings_value_too_long() -> hikari.Embed:
  #   return embed(
  #     'Invalid setting value.',
  #     f'Setting value cannot be longer than {SETTINGS_VALUE_MAX_LENGTH} characters.',
  #     color=S.EMBED_COLORS['error'],
  #   )

  @staticmethod
  def fuck_confirm(rem: Reminder) -> hikari.Embed:
    return embed(
      'Are you sure you want to cancel the latest reminder?',
      f'You set this reminder {tcr.discord.IFYs.timeify(rem.created_at, style="R")} which is why I am asking you to confirm if you intended to cancel it. Click `Yes` to cancel the reminder, or `No` to keep it.',
      color=S.EMBED_COLORS['cancelled'],
    )

  @staticmethod
  def invalid_snowflake(user_id: int) -> hikari.Embed:
    return embed(
      'Invalid snowflake',
      f'`{user_id}` is not a valid snowflake',
      color=S.EMBED_COLORS['error'],
    )

  @staticmethod
  def not_registered_in_db(user_id: int, *, you_are: bool = False) -> hikari.Embed:
    if not tcr.discord.is_snowflake(user_id, allow_string=True):
      return EMBED.invalid_snowflake(user_id)

    return embed(
      'Not registered in the database',
      f"{'You are' if you_are else 'This user is'} not registered in the database: {tcr.discord.IFYs.userify(user_id)}",
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
  def banned(**kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> tcr.discord.types.HikariDictMessage:
    return {
      'content': ':x: You are banned from using this bot.',
      'flags': hikari.MessageFlag.EPHEMERAL,
      **kwargs,
    }

  @staticmethod
  def reminder_list(r: t.Iterable[Reminder], archive: bool = False, **kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> nav.NavigatorView:
    """List of user's reminders.

    After that:
    ```py
    builder = await navigator.build_response_async(ACL)
    await builder.send_to_channel(channel_id)
    ACL.start_view(navigator)
    ```
    """
    pages = []

    for remslice in tcr.batched(list(enumerate(r, start=1)), S.REMINDER_LIST_REMINDERS_PER_PAGE, back_to_front=True) or [[]]:
      pages.append(nav.Page(embed=EMBED.reminder_list(remslice, len(r), archive=archive)))

    REMINDER_LIST_NAVBAR_ITEMS = [
      m_components.PrevNavButton(),
      m_components.NextNavButton(),
    ]

    return nav.NavigatorView(pages=pages, items=(REMINDER_LIST_NAVBAR_ITEMS if (len(pages) > 1) else []), **kwargs)

  @staticmethod
  def reminder(rem: Reminder) -> tcr.discord.types.HikariDictMessage:
    user_mentions = []

    if rem.is_flag(CTF.IMPORTANT):
      content = f'# {tcr.discord.IFYs.userify(rem.user)}'
      user_mentions.append(rem.user)
    else:
      content = hikari.UNDEFINED

    return {
      'content': content,
      'embed': m_embed.EMBED.reminder(rem),
      'attachments': rem.attachments,
      'user_mentions': user_mentions,
    }

  @staticmethod
  def reminder_safemode(rem: Reminder, e: hikari.HikariError) -> tcr.discord.types.HikariDictMessage:
    parts = [
      f"""
# There was an issue sending your reminder therefore a fallback method has been triggered.
# Cause of this incident: {tcr.extract_error(e)}
"""[1:-1],
      rem.text,
    ]

    if rem.attachments:
      msg = f"Your message contained attachments, them failing to attach might be the cause of this issue, here's a list of their URLs:\n"
      msg += '\n'.join([f'- {x.url}' for x in rem.attachments])
      parts.append(msg)

    parts.append(
      f'Sorry for iconvenience! You can report this as a bug to the developer, contact: {S.CREATED_BY_STR!s}\n'
      'In raw_reminder.json you can see the export of this single reminder, if you wish to recover any raw data, please send it along in case of reporting this as a bug.'
    )

    reminder_txt = hikari.Bytes('\n\n'.join(parts).encode('utf-8'), 'reminder.txt')
    reminder_raw_json = hikari.Bytes(tcr.fmt_iterable(rem.export(force_export_even_if_hidden=True)), 'reminder_raw.json')

    return {
      'embed': EMBED.reminder_safemode(),
      'attachments': [reminder_txt, reminder_raw_json],
    }

  @staticmethod
  def not_my_message(do_what: str = 'do that', **kwargs: Unpack[tcr.discord.types.HikariDictMessage]) -> tcr.discord.types.HikariDictMessage:
    return {
      'content': f"{S.NO} I can't {do_what} to a message I didn't send!.",
      'flags': hikari.MessageFlag.EPHEMERAL,
      **kwargs,
    }
