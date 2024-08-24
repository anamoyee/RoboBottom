from r11_tasks import *

YOU_DONT_HAVE_ANY_REMINDERS_TO = "You don't have any reminders to %s. Schedule a reminder like this: `30m finish this bot`"


async def _wrong_index(r: list[Reminder], responder: Callable[[hikari.Embed], Coroutine], verb: str, flags=hikari.MessageFlag.NONE):
  desc = f'Choose an index from range: `1-{len(r)}`' if r else YOU_DONT_HAVE_ANY_REMINDERS_TO % verb
  return await responder(EMBED.generic_text_error('Invalid index', desc), flags=flags)


async def rd_run(
  responder: tcrd.types.HikariResponder,
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

  out = tcrd.discord_error(result) if errored else tcrd.codeblock(tcr.fmt_iterable(result), langcode='py')

  await responder(out)


async def rd_ban(
  responder: tcrd.types.HikariResponder,
  *,
  admin_id: int,
  user: int,
  unban: bool,
  drop_db: bool,
):
  if not tcrd.is_snowflake(user, allow_string=True):
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
  await responder(f'{message} {tcrd.IFYs.userify(user)}{suffix}', flags=hikari.MessageFlag.EPHEMERAL)


if True:  # rd_dev_...

  async def rd_dev_now(*, responder: tcrd.types.HikariResponder, user_id: int, idx: int):
    if not Database.exists(user_id):
      await responder(EMBED.not_registered_in_db(user_id), flags=hikari.MessageFlag.EPHEMERAL)
      return

    db: U = Database(user_id)
    try:
      idx = user_facing_to_python_r_idx(db['r'], idx)
    except IndexError:
      await _wrong_index(db['r'], responder, 'dev-now', flags=hikari.MessageFlag.EPHEMERAL)
      return
    else:
      rem = db['r'][idx]
      rem.remove_from_db(db)
      await rem.send()
      await responder(f'{S.YES}', flags=hikari.MessageFlag.EPHEMERAL)

  async def rd_dev_get(*, responder: tcrd.types.HikariResponder, user_id: int, idx: int):
    if not Database.exists(user_id):
      await responder(EMBED.not_registered_in_db(user_id), flags=hikari.MessageFlag.EPHEMERAL)
      return

    db: U = Database(user_id)
    try:
      idx = user_facing_to_python_r_idx(db['r'], idx)
    except IndexError:
      await _wrong_index(db['r'], responder, 'dev-now', flags=hikari.MessageFlag.EPHEMERAL)
      return
    else:
      await responder(tcrd.codeblock(tcr.fmt_iterable(db['r'][idx], syntax_highlighting=False), langcode='py'), flags=hikari.MessageFlag.EPHEMERAL)

  async def rd_dev_guilds(*, responder: tcrd.types.HikariResponder):
    count = await get_guild_count(force_refetch=True)

    await debugpond(responder, count, flags=hikari.MessageFlag.EPHEMERAL)

  async def rd_dev_users(*, responder: tcrd.types.HikariResponder):
    users = Database.iter_all_path_names()
    users = list(users)

    await responder(
      tcrd.codeblocks(
        str(len(users)),
        tcr.fmt_iterable(users, syntax_highlighting=False),
        langcodes=('py', 'py'),
      ),
      flags=hikari.MessageFlag.EPHEMERAL,
    )


async def r_remind(
  responder: tcrd.types.HikariResponder,
  text: str,
  *,
  user: int,
  ctx_or_event: arc.Context | hikari.GuildMessageCreateEvent,
  replyto: hikari.PartialMessage | None = None,
) -> None:
  """### R: Schedule a reminder on behalf of the invoker."""

  COUNT_DELAY_FROM_MESSAGE_ARRIVAL = text.startswith('^')
  text = text.removeprefix('^')

  if replyto:
    if ' ' not in text:
      text += ' '

    if not replyto.content or (replyto.embeds and replyto.embeds[0].description):
      reply_content = None
    else:
      reply_content = replyto.content if replyto.content != '`' else ''

    if reply_content is not None:
      text += reply_content
    else:
      text += replyto.embeds[0].description

  try:
    kwargs = {}
    if COUNT_DELAY_FROM_MESSAGE_ARRIVAL:
      timestamp = snap_datetime_to_nearest_minute(replyto.timestamp)

      kwargs['now_unix'] = round(timestamp.timestamp())

    rem = build_reminder(user, text, ctx_or_event=ctx_or_event, **kwargs)
  except TextErrpondError as e:
    await e.execute(ctx_or_event)
    return

  try:
    Database(user).append_reminder(rem)
  except TextErrpondError as e:
    await e.execute(ctx_or_event)

  out = S.SCHEDULED_SUCCESSFULLY_PROMPT.replace('{random_sure}', random_sure()).replace('{time}', TIMESTR.to_str(rem.offset))

  await responder(out, flags=flags_hide_on_guild(ctx_or_event))


async def r_list(
  user: int,
  channel: hikari.SnowflakeishOr[hikari.TextableChannel],
  *,
  text: str,
  archive: bool,
):
  """### R: Send a list of user's reminders."""
  channel = await BOT.rest.create_dm_channel(user)

  db: U = Database(user)

  if archive:
    r = db['archive']
  else:
    r = db['r']

  navigator: nav.NavigatorView = RESP.reminder_list(r, archive=archive)

  builder = await navigator.build_response_async(MCL, start_at=len(navigator.pages) - 1)
  await builder.send_to_channel(channel=channel)
  if navigator.children:  # To prevent a warning of an empty navigator being started
    MCL.start_view(navigator)


async def r_cancel(
  responder: tcrd.types.HikariResponder,
  user: int,
  text: str,
  *,
  archive: bool,
):
  """### R: Cancel a reminder."""

  db: U = Database(user)

  if archive:
    r = db['archive']
  else:
    r = db['r']

  try:
    rem = r.pop(user_facing_to_python_r_idx(r, text))
  except IndexError:
    return await _wrong_index(r, responder, 'cancel')

  if archive:
    db['archive'] = r
  else:
    db['r'] = r

  try:
    await respond_with_attachments_or_send_urls_as_file(responder, EMBED.reminder_canceled(rem, archive=archive), attachments=hidden_or(rem, rem.attachments))
  except Exception:
    await responder(somehow_you_managed_to('break the code that lets you view the reminder after it has been cancelled'))
    if testmode():
      raise


async def r_view(
  responder: tcrd.types.HikariResponder,
  user: int,
  text: str,
  *,
  archive: bool,
):
  """### R: View a reminder as embed and send."""

  db: U = Database(user)
  if archive:
    r = db['archive']
  else:
    r = db['r']

  try:
    idx = user_facing_to_python_r_idx(r, text)
    rem = r[idx]
    idx = r.index(rem)
  except IndexError:
    return await _wrong_index(r, responder, 'view')

  try:
    await respond_with_attachments_or_send_urls_as_file(responder, EMBED.reminder_view(rem, idx, archive=archive), attachments=hidden_or(rem, rem.attachments))
  except Exception:
    await responder(somehow_you_managed_to('break the code that lets you view the reminder'))
    if testmode():
      raise


async def r_fuck(
  responder: tcrd.types.HikariResponder,
  message: hikari.Message,
  user: int,
):
  """### R: Cancel last scheduled reminder - add a confirmation if it was long ago."""

  db: U = Database(user)

  if db['r']:

    def key_recently_scheduled(rem: Reminder):
      return rem.created_at

    rem = sorted(db['r'], key=key_recently_scheduled, reverse=True)[0]

    async def canceling_callback(_: miru.Button = None, ctx: miru.ViewContext = None, *, responder=responder, rem=rem, message=message):
      rem.remove_from_db()
      await responder(EMBED.reminder_canceled(rem), reply=message if ctx is None else ctx.message)

    if (int(time.time()) - rem.created_at) >= S.SUSPICIOUS_RIPPLE_CANCEL_TIME:
      await tcrd.confirm(
        responder,
        MCL,
        yes_callback=canceling_callback,
        no_callback=tcr.avoid,
        disable_on_click=True,
        responder_kwargs={
          'embeds': [EMBED.fuck_confirm(rem), EMBED.reminder_view(rem)],
          'reply': message,
        },
      )
    else:
      await canceling_callback()

  else:
    await responder(EMBED.generic_text_error('No reminders to cancel', YOU_DONT_HAVE_ANY_REMINDERS_TO % 'cancel'), reply=message)


async def rr_del(
  responder: tcrd.types.HikariResponder,
  message: hikari.Message,
  referenced: hikari.PartialMessage,
):
  """### R(Reply): Delete this message if it's authored by this bot."""

  if referenced.author.id == BOT.get_me().id:
    with contextlib.suppress(hikari.NotFoundError):
      await referenced.delete()
  else:
    await responder(**RESP.not_my_message(reply=message))
