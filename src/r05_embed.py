from r04_bot import *


# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
# ! Configure embeds & responses in the settings menu first, then here if the setting you wish to change is not there.
class EMBED:
  @staticmethod
  def generic_error(e: Exception, color=S.EMBED_COLORS['error'], **kwargs) -> hikari.Embed:
    return embed(
      *tcr.extract_error(e, raw=True),
      color=color,
      **kwargs,
    )

  @staticmethod
  def reminder(reminder: Reminder) -> hikari.Embed:
    return embed(
      description=reminder.text,
      **S.REMINDER_EMBED,
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
