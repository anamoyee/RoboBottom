from r11_tasks import *


async def rd_run(
  responder: Callable[[str], Coroutine],
  code: str,
  *,
  do_await: bool = True,
  do_exec: bool = False,
) -> None:
  """## Warning: assuming invoker is authorised.

  ### RD: Run python text as code, then call the responder with a nicely discord-formatted result.

  Supports error handling. Will respond with a proper error result if any errors occur.
  """

  if do_await:
    awaitable, code = code.startswith('await '), code.removeprefix('await ')

  try:
    if do_exec:
      exec_dict = {}
      exec(code, globals(), exec_dict)
      result = exec_dict.get('_')
    else:
      result = eval(code)

    if do_await and awaitable:
      result = await result
  except Exception as e:
    result = e
    errored = True
  else:
    errored = False

  out = tcr.discord_error(result) if errored else tcr.codeblock(tcr.fmt_iterable(result), langcode='py')

  await responder(out)


async def rd_ban(
  responder: Callable[[str], Coroutine],
  *,
  admin_id: int,
  user: int,
  unban: bool,
  drop_db: bool,
):
  if not tcr.discord.is_snowflake(user, allow_string=True):
    await responder(f""":x: Invalid user ID: `{user.replace('`', "'")}`""", flags=hikari.MessageFlag.EPHEMERAL)
    return

  if unban and drop_db:
    await responder(':x: Cannot `unban` and `wipedb` at the same time bruh???', flags=hikari.MessageFlag.EPHEMERAL)
    return

  user = int(user)

  if not unban and user == admin_id:
    await responder(":x: You can't ban yourself...", flags=hikari.MessageFlag.EPHEMERAL)
    return

  banned = GDB['banned']

  suffix = ''

  if drop_db:
    udb: U | Database = Database(user)
    udb.drop_db()
    suffix += ' and dropped their database'

  if user in banned:
    if unban:
      banned.remove(user)
      message = f'{S.YES} Unbanned'
    else:
      message = f'{S.WARN} User already banned:'
  else:
    if unban:
      message = f'{S.WARN} User was not banned:'
    else:
      banned.add(user)
      message = ':hammer: Banned'
  GDB['banned'] = banned
  await responder(f'{message} {tcr.discord.IFYs.userify(user)}{suffix}', flags=hikari.MessageFlag.EPHEMERAL)


async def r_remind(
  responder: Callable[[str], Coroutine],
  text: str,
  *,
  user: int,
  ctx_or_event: arc.Context | hikari.GuildMessageCreateEvent,
  replyto: hikari.PartialMessage | None = None,
) -> None:
  """### R: Schedule a reminder on behalf of the invoker.

  Args:
    responder: The responder to call with the discord message.
    text: The reminder text.
    user: The discord user ID of the reminder's owner.
  """

  if replyto:
    if ' ' not in text:
      text += ' '

    if not replyto.content:
      reply_content = None
    else:
      reply_content = replyto.content if replyto.content != '`' else ''

    if reply_content is not None:
      text += reply_content
    else:
      text += replyto.embeds[0].description
  try:
    rem = build_reminder(user, text, ctx_or_event=ctx_or_event)
  except TextErrpondError as e:
    await e.execute(ctx_or_event)
    return

  try:
    Database(user).append_reminder(rem)
  except TextErrpondError as e:
    await e.execute(ctx_or_event)

  out = S.SCHEDULED_SUCCESSFULLY_PROMPT.replace('{random_sure}', random_sure()).replace('{time}', TIMESTR.to_str(rem.offset))

  await responder(out, flags=flags_hide_on_guild(ctx_or_event))


async def r_viewlist(
  user: int,
  channel: hikari.SnowflakeishOr[hikari.TextableChannel],
):
  """Send a list of user's reminders."""
  channel = await BOT.rest.create_dm_channel(user)

  db: U = Database(user)

  r = db['r']

  navigator: nav.NavigatorView = RESP.reminder_list(r)

  builder = await navigator.build_response_async(MCL, start_at=len(navigator.pages) - 1)
  await builder.send_to_channel(channel=channel)
  if navigator.children:  # To prevent a warning of an empty navigator being started
    MCL.start_view(navigator)


async def _wrong_index(r: list[Reminder], responder: Callable[[hikari.Embed], Coroutine], verb: str):
  desc = f'Choose an index from range: `1-{len(r)}`' if r else f"You don't have any reminders to {verb}. Schedule a reminder like this: `30m finish this bot`"
  return await responder(EMBED.generic_text_error('Invalid index', desc))


async def r_cancel(
  responder: Callable[[str], Coroutine],
  user: int,
  text: str,
):
  """### R: Cancel a reminder."""

  db: U = Database(user)
  r = db['r']

  if able_result := tcr.able(int, text):
    idx = able_result
  else:
    await _wrong_index(r, responder, 'cancel')

  try:
    rem = r.pop(idx)
  except IndexError:
    return await _wrong_index(r, responder, 'cancel')

  await responder(EMBED.reminder_canceled(rem))


async def r_view(
  responder: Callable[[str], Coroutine],
  user: int,
  text: str,
):
  """### R: View a reminder as embed and send."""

  db: U = Database(user)
  r = db['r']

  if not (_a := tcr.able(int, text)):
    return await _wrong_index(r, responder, 'view')
  else:
    idx = _a.result

  try:
    if idx < 0:
      rem = r[idx]
    else:
      rem = r[idx - 1]
  except IndexError:
    return await _wrong_index(r, responder, 'view')
  else:
    return await responder(EMBED.reminder_view(rem))


async def rr_del(
  responder: Callable[[str], Coroutine],
  message: hikari.Message,
  referenced: hikari.PartialMessage,
):
  """### R(Reply): Delete this message if it's authored by this bot."""

  if referenced.author.id == BOT.get_me().id:
    with contextlib.suppress(hikari.NotFoundError):
      await referenced.delete()
  else:
    await responder(**RESP.not_my_message(reply=message))
