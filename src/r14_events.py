from r13_slash import *


@BOT.listen(hikari.StartingEvent)
async def onStartingEvent(event: hikari.StartingEvent): ...


@BOT.listen(hikari.StartedEvent)
async def onStartedEvent(event: hikari.StartedEvent):
  if True:  # Start Tasks
    task_reminder.start()
    task_backup.start()
    c.log('All tasks started')


@BOT.listen(hikari.StoppingEvent)
async def onStoppingEvent(event: hikari.StoppingEvent):
  if True:  # Stop Tasks
    for task in TASKS:
      task.stop()

    while task_reminder._task and not task_reminder._task.done():
      await asyncio.sleep(0.1)

    c.log(f'Task shutdown status: {tcr.fmt_iterable([task._task.done() if task._task else True for task in TASKS], syntax_highlighting=True).replace("True", "OK").replace("False", "FAILED")}')


@BOT.listen(arc.StoppingEvent)
async def onArcStoppingEvent(event: arc.StoppingEvent): ...


@BOT.listen(hikari.StoppedEvent)
async def onStoppedEvent(event: hikari.StoppedEvent): ...


@BOT.listen(hikari.DMMessageCreateEvent)
@event_uncaught_error_handler_decorator
async def onDMMessageCreateEvent(event: hikari.DMMessageCreateEvent):
  if not event.is_human:
    return

  if event.content and event.content == 'unban':  # Failsafe
    await rd_ban(event.message.respond, admin_id=event.author.id, user=event.author.id, unban=True, drop_db=False)
    return

  if event.content and event.content in P.DM_CMD_ALIASES('del') and event.message.referenced_message:
    await rr_del(event.message.respond, event.message, event.message.referenced_message)
    return

  if event.author.id in GDB['banned']:
    await event.message.respond(**RESP.banned(), reply=event.message)
    return

  scontent = event.content or ''

  if ((' ' not in scontent.strip()) or (' ' in scontent[:-1].strip())) and scontent[-1] in S.ACCIDENTAL_SUFFIXES:
    scontent = scontent[:-1]

  scontent = scontent.strip()

  if not scontent:
    if event.message.attachments:
      await event.message.respond(EMBED.generic_text_error('Empty message', 'You sent a message with a file, but no text, therefore no reminder delay can be inferred.'))
    return

  identifier = (scontent + ' ').split(' ', maxsplit=1)[0]

  def startswith_and_strip(s: str, aliases: list[str]) -> str | Literal[False]:
    for alias in aliases:
      if s.startswith(alias):
        return tcr.types.AlwaysTruthyStr(s.removeprefix(alias).strip())
    return False

  if text := startswith_and_strip(scontent, P.DM_CMD_ALIASES('list')):
    await r_list(event.author.id, event.channel_id, archive=text.startswith(S.ARCHIVE_SUFFIX), text=text.removeprefix(S.ARCHIVE_SUFFIX))
    return
  elif text := startswith_and_strip(scontent, P.DM_CMD_ALIASES('cancel')):
    await r_cancel(event.message.respond, event.author.id, text.removeprefix(S.ARCHIVE_SUFFIX), archive=text.startswith(S.ARCHIVE_SUFFIX))
    return
  elif text := startswith_and_strip(scontent, P.DM_CMD_ALIASES('view')):
    await r_view(event.message.respond, event.author.id, text.removeprefix(S.ARCHIVE_SUFFIX), archive=text.startswith(S.ARCHIVE_SUFFIX))
    return
  elif identifier in P.DM_CMD_ALIASES('fuck'):
    await r_fuck(event.message.respond, event.message, event.author.id)
    return
  else:
    await r_remind(event.message.respond, scontent, user=event.author.id, ctx_or_event=event, replyto=event.message.referenced_message)
    return
