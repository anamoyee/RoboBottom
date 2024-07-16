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
  return hikari.MessageFlag.EPHEMERAL if (hasattr(ctx_or_event, 'guild_id') and ctx_or_event.guild_id is not None) else hikari.MessageFlag.NONE


def please_tell_me_how_you(what: str = 'did this') -> str:
  return f'Please tell me how you {what}, DM me: <@{S.CREATED_BY["id"]}> (or add me as friend on discord @{S.CREATED_BY["name"]} if you can\'t click on the mention)'


def somehow_you_managed_to(do_what: str, *, about_to: bool = False) -> str:
  if about_to:
    return f'{S.NO} Somehow you were about to {do_what} (you were about to trigger a bug).\n{please_tell_me_how_you("did this")}'
  else:
    return f'{S.NO} Somehow you managed to {do_what} (you triggered a bug).\n{please_tell_me_how_you("did this")}'


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
  except Exception as e:
    raise TextErrpondError('Invalid time', tcr.codeblock(tcr.extract_error(e), langcode='')) from e

  if not testmode() and offset <= 0:
    raise TextErrpondError('Invalid time', f'You cannot set a negative or zero delay.')

  if not testmode() and offset < S.MIN_REMINDER_TIME:
    raise TextErrpondError('Invalid time', f'You cannot set a time shorter than **`{TIMESTR.to_str(S.MIN_REMINDER_TIME)}`**')

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


def user_facing_to_python_r_idx(r: list[Reminder], idx_text: str) -> int:
  """Convert a user-inputed index to a reminder list index. For example `'1'`->`0`, `'-1'` -> `-1`.

  Raise IndexError if no reminder at that index is found.
  """
  if not (_a := tcr.able(int, idx_text)):
    raise IndexError('Invalid index. Unable to convert to int.')

  idx = _a.result

  if idx == 0:
    raise IndexError('Invalid index. Zero not allowed.')

  if idx > 0:
    idx -= 1

  r[idx]
  return idx


@tcr.timeit
def backup_all_databases() -> p.Path:
  if not S.DB_DIRECTORY_BACKUP.exists():
    S.DB_DIRECTORY_BACKUP.mkdir(parents=True)

  if not S.DB_DIRECTORY.exists():
    raise RuntimeError('Database directory missing on backup')

  max_items = S.MAX_BACKUPS_BEFORE_DELETING_OLDEST - 1

  current_time_corrected = datetime.datetime.now(tz=S.GLOBAL_TIMEZONE) + datetime.timedelta(
    seconds=30
  )  # Shifted forward by 30s due to issues with it being sth like 23:59:59 the previous day and seconds are cut off in the default format specifier anyway
  current_time_str = current_time_corrected.strftime(S.BACKUP_DIRECTORY_NAME_FORMAT)

  items = list(S.DB_DIRECTORY_BACKUP.iterdir())
  found = len(items)

  if S.MAX_BACKUPS_BEFORE_DELETING_OLDEST > 0 and found > max_items:
    c.log(f'Deleting old backup(s) due to policy of max {S.MAX_BACKUPS_BEFORE_DELETING_OLDEST} backups ({found} found + the one being made right now)')
    items_with_ctime = [(item, item.stat().st_ctime) for item in items]
    items_with_ctime.sort(key=lambda x: x[1])
    num_to_remove = len(items) - max_items
    for item, _ in items_with_ctime[:num_to_remove]:
      c.log(f'  rm {item}')
      if item.is_dir():
        shutil.rmtree(item)
      else:
        item.unlink()

  backup_path = S.DB_DIRECTORY_BACKUP / current_time_str

  shutil.copytree(S.DB_DIRECTORY, backup_path)

  return backup_path


NEW_INSTANCE_OF_IFVISIBLE = object()


def hidden_or(rem: Reminder, ifvisible, ifhidden=NEW_INSTANCE_OF_IFVISIBLE):
  if rem.is_flag(CTF.HASH_HIDDEN):
    return ifhidden if ifhidden is not NEW_INSTANCE_OF_IFVISIBLE else type(ifvisible)()
  else:
    return ifvisible


def get_slash_command_mentions() -> tcr.discord.types.CommandIDsDict[str, hikari.Snowflake]:
  if not hasattr(get_slash_command_mentions, '_slash_command_mentions'):
    get_slash_command_mentions._slash_command_mentions = tcr.discord.get_slash_command_ids(ACL)

  return get_slash_command_mentions._slash_command_mentions
