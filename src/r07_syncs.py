from r06_db import *


def testmode(*, dash=True) -> str:
  return f'{" - " if dash else ""}Testmode' if TESTMODE else ''


def author_dict(
  who: hikari.OwnUser | hikari.User | None = None,
  url: str | None = None,
  *,
  displayname: bool = False,
) -> dict:
  if who is None:
    who = BOT.get_me()

  dick = {
    'name': who.username if not displayname else tcr.getattr_queue(who, 'display_name', 'username'),
    'icon': who.avatar_url or who.default_avatar_url,
  }

  if url:
    dick.update({'url': url})

  return dick


def random_sure() -> str:
  return rng.choice(S.RANDOM_SURES)


def flags_hide_on_guild(ctx_or_event: arc.GatewayContext | hikari.GuildMessageCreateEvent) -> Literal[hikari.MessageFlag.NONE, hikari.MessageFlag.EPHEMERAL]:
  """Return `hikari.MessageFlag.EPHEMERAL` if request originated from a guild, else `hikari.MessageFlag.NONE`."""
  return hikari.MessageFlag.EPHEMERAL if (isinstance(ctx_or_event, hikari.GuildMessageCreateEvent) and hasattr(ctx_or_event, 'guild_id')) else hikari.MessageFlag.NONE


def somehow_you_managed_to(do_what: str, *, about_to: bool = False) -> str:
  if about_to:
    return f'Somehow you were about to {do_what}, please tell me how you managed to do it, DM me: <@{S.CREATED_BY["id"]}> (or add me as friend on discord @{S.CREATED_BY["name"]} if you can\'t click on the mention)'
  else:
    return f'Somehow you managed to {do_what}, please tell me how you did this, DM me: <@{S.CREATED_BY["id"]}> (or add me as friend on discord @{S.CREATED_BY["name"]} if you can\'t click on the mention)'


def build_reminder(
  user: int,
  text: str,
  *,
  ctx_or_event: arc.Context | hikari.GuildMessageCreateEvent,
) -> Reminder:
  """Return an instance of Reminder, may raise TextErrpondError."""
  if ' ' not in text:  # '1h' -> '1h 1h'
    text = f'{text} {text}'

  attachments: t.Sequence[hikari.Attachment] = tcr.getattr_queue(ctx_or_event, 'message.attachments', default=())

  tstr, content = text.split(' ', maxsplit=1)  # Split time from content
  if '&' in tstr:
    tstr, recursion_tstr = tstr.split('&', maxsplit=1)
  else:
    recursion_tstr = ''

  flags = CTF.NONE
  while tstr and tstr[0] in CTF_DICT:  # Detect any flags from the beginning of the tstr (eg: '!#') and or them into the flags while removing them from tstr in the process.
    flags |= CTF_DICT[tstr[0]]  # BEFORE: tstr='#1h' flags=CTF.NONE
    tstr = tstr[1:]  # AFTER:  tstr='1h'  flags=CTF.HASH_HIDDEN

  try:
    offset = TIMESTR.to_int(tstr)

    if offset < S.MINIMUM_REMINDER_TIME:
      raise TimeoutError
  except TimeoutError as e:
    raise TextErrpondError('Invalid time', f'You cannot set a time shorter than **`{TIMESTR.to_str(S.MINIMUM_REMINDER_TIME)}`**') from e
  except tcr.error.ConfigurationError as e:
    raise TextErrpondError('Invalid time', 'Time must be strictly positive') from e
  except Exception as e:
    raise TextErrpondError('Invalid time', tcr.codeblock(tcr.extract_error(e), langcode='')) from e

  return Reminder(
    user=user,
    unix=time.time() + offset,
    text=content,
    tstr=tstr,
    offset=offset,
    flags=flags,
    ctx_message_id=ctx_or_event.message.id if isinstance(ctx_or_event, hikari.GuildMessageCreateEvent) else None,
    recursion_tstr=recursion_tstr,
    attachments=attachments,
  )


def did_as_i_said(s: str) -> bool:
  return s == 'Yes, do as I say!'
