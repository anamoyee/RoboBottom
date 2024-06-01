from r13_slash import *


@BOT.listen(hikari.StartingEvent)
async def onStartingEvent(event: hikari.StartingEvent): ...


@BOT.listen(hikari.StartedEvent)
async def onStartedEvent(event: hikari.StartedEvent):
  if True:  # Guild Count
    global GUILD_COUNT
    GUILD_COUNT = await get_guild_count()

  if True:  # Start Tasks
    task_reminder.start(bot=BOT, acl=ACL)
    task_backup.start()
    c.log('All tasks started')


@BOT.listen(hikari.StoppingEvent)
async def onStoppingEvent(event: hikari.StoppingEvent):
  if True:  # Stop Tasks
    for task in TASKS:
      task.stop()
    c.log('All tasks stopped')


@BOT.listen(arc.StoppingEvent)
async def onArcStoppingEvent(event: arc.StoppingEvent): ...


@BOT.listen(hikari.StoppedEvent)
async def onStoppedEvent(event: hikari.StoppedEvent): ...


@BOT.listen(hikari.DMMessageCreateEvent)
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
  if scontent and scontent[-1] in S.ACCIDENTAL_SUFFIXES:
    scontent = scontent[:-1]

  if not scontent:
    if event.message.attachments:
      await event.message.respond(EMBED.generic_text_error('Empty message', 'You sent a message with a file, but no text, therefore no reminder delay can be inferred.'))
    return

  identifier = (scontent + ' ').split(' ', maxsplit=1)[0]
  scontent_without_identifier = scontent.removeprefix(identifier)

  if scontent in P.DM_CMD_ALIASES('list'):
    await r_viewlist(event.author.id, event.channel_id)
    return
  elif identifier in P.DM_CMD_ALIASES('cancel'):
    await r_cancel(event.message.respond, event.author.id, scontent_without_identifier)
    return
  elif identifier in P.DM_CMD_ALIASES('view'):
    await r_view(event.message.respond, event.author.id, scontent_without_identifier)
    return
  else:
    await r_remind(event.message.respond, scontent, user=event.author.id, ctx_or_event=event, replyto=event.message.referenced_message)
    return
