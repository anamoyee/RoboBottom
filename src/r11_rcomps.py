from r10_tasks import *


async def r_cancel(event: hikari.DMMessageCreateEvent, content: str):
  event.message.respond('Not implemented')


async def r_view(event: hikari.DMMessageCreateEvent, content: str):
  event.message.respond('Not implemented')


async def r_reminder(respond: Callable, author_id: int, content: str):
  flags = 0

  while content[0] in CTFLookup:
    flags |= CTFLookup[content[0]]
    content = content[1:]

  if ' ' not in content:
    content = f'{content} {content}'

  t, content = content.split(' ', maxsplit=1)

  try:
    t_int = TIMESTR.to_int(t)
  except (ValueError, tcr.error.ConfigurationError):
    return await respond(EMBED.generic_error(ValueError('Invalid timestr')))

  reminder = Reminder(
    user=author_id,
    unix=int(time.time() + t_int),
    created_at=int(time.time()),
    text=content,
    tstr=t,
    flags=flags,
  )

  add_reminder_to_user(reminder)

  await respond(S.SCHEDULED_SUCCESSFULLY_PROMPT.replace('{random_sure}', random_sure()).replace('{time}', TIMESTR.to_str(t_int)))
