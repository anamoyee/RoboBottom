from r12_slash import *


@BOT.listen(hikari.StartingEvent)
async def onStartingEvent(event: hikari.StartingEvent): ...


@BOT.listen(hikari.StartedEvent)
async def onStartedEvent(event: hikari.StartedEvent):
  with contextlib.suppress(ModuleNotFoundError):
    __import__('rich.traceback').traceback.install()

  if True:  # Guild Count
    global GUILD_COUNT
    GUILD_COUNT = await get_guild_count()

  if True:  # Task starters
    reminder_task.start()
    c.log('All tasks started.')

  if True:  # Update Revolution
    global REVOLUTION
    with shelve.open(get_db('v')) as shelf:
      REVOLUTION = shelf.get('revolution', 0) + 1
      shelf['revolution'] = REVOLUTION

  if True:  # clog Header
    me = BOT.get_me()
    [
      c.log(x)
      for x in (
        f"""
========================================
Running on Python {'.'.join([str(x) for x in sys.version_info[:2]])}
Started {me.username}#{me.discriminator} v{VERSION}
Status:   {S.STATUS:>30}
Activity: {S.ACTIVITY.name:>30}
On the eve of our {Style.UNDERLINE}{tcr.nth(REVOLUTION)}{Style.RESET + Fore.GREEN + Style.BOLD} revolution...
========================================
"""[1:-1]
      ).split('\n')
    ]


@BOT.listen(hikari.StoppingEvent)
async def onStoppingEvent(event: hikari.StoppingEvent):
  reminder_task.cancel()
  c.log('All tasks stopped.')


@BOT.listen(hikari.StoppedEvent)
async def onStoppedEvent(event: hikari.StoppedEvent): ...


@BOT.listen(hikari.DMMessageCreateEvent)
async def onDMMessageCreateEvent(event: hikari.DMMessageCreateEvent):
  if event.is_bot:
    return None

  if not event.content:
    return None

  match event.content[0]:
    case 'c':
      return await r_cancel(event, event.content[1:])
    case 'v':
      return await r_view(event, event.content[1:])
    case _:
      return await r_reminder(event.message.respond, event.author_id, event.content)
