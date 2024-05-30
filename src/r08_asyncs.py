from r07_syncs import *


async def get_guild_count(*, printout: bool = True, force_refetch: bool = False):
  if force_refetch or not hasattr(get_guild_count, '_guild_count'):
    get_guild_count._guild_count = await fetch_guild_count(printout=printout)
  return get_guild_count._guild_count


async def fetch_guild_count(*, printout: bool = True):
  count = len(await BOT.rest.fetch_my_guilds())
  if printout:
    c.log(f'Fetched guild count: {count}')
  return count


async def errpond(
  ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent, e: str | Exception = '', embed_color: int = S.EMBED_COLORS['error'], flags=hikari.MessageFlag.EPHEMERAL, **responder_kwargs
):
  if not e:
    e = 'No further information provided'
  responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)
  return await responder(
    embed('An error occured' if isinstance(e, str) else tcr.extract_error(e), e if isinstance(e, str) else tcr.codeblock(tcr.extract_traceback(e), langcode='py'), color=embed_color),
    flags=flags,
    **responder_kwargs,
  )


async def text_errpond(
  ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent,
  title: str,
  description: str = 'No further information provided',
  embed_callable: Callable = EMBED.generic_text_error,
  flags=hikari.MessageFlag.EPHEMERAL,
  **responder_kwargs,
):
  responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)

  return await responder(embed_callable(title, description), flags=flags, **responder_kwargs)


async def debugpond(ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent, obj: Any, flags=hikari.MessageFlag.EPHEMERAL, **responder_kwargs):
  responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)
  return await responder(tcr.codeblock(tcr.fmt_iterable(obj), langcode='py'), flags=flags, **responder_kwargs)
