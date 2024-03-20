from r06_syncs import *


async def get_guild_count():
  return len(await BOT.rest.fetch_my_guilds())


async def errpond(ctx: arc.GatewayContext, e: str | Exception = '', flags=hikari.MessageFlag.EPHEMERAL):
  if not e:
    e = 'No further information provided'
  responder = tcr.getattr_queue(ctx, 'respond', default=ctx)
  return await responder(
    embed('An error occured' if isinstance(e, str) else tcr.extract_error(e), e if isinstance(e, str) else tcr.codeblock(tcr.extract_traceback(e), langcode='py'), color=S.EMBED_COLORS['error']),
    flags=flags,
  )


if True:  # Reminder Asyncs

  async def trigger_reminder(reminder: Reminder, *, delete=True):
    """Send the reminder body to the user, remove reminder from their remlist if delete=True.

    This may raise hikari errors if send fails.
    """
    channel = await BOT.rest.create_dm_channel(reminder.user)
    await channel.send(EMBED.reminder(reminder))

    if delete:
      delete_reminder_by_reminder(reminder)
