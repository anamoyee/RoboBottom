from r07_syncs import *

if True:  # Guild count

  async def get_guild_count(*, printout: bool = True, force_refetch: bool = False):
    if force_refetch or not hasattr(get_guild_count, '_guild_count'):
      get_guild_count._guild_count = await fetch_guild_count(printout=printout)
    return get_guild_count._guild_count

  async def fetch_guild_count(*, printout: bool = True):
    count = len(await BOT.rest.fetch_my_guilds())
    if printout:
      c.log(f'Fetched guild count: {count}')
    return count


if True:  # Custom responders

  async def errpond(
    ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent | Callable[[Unpack[tcrd.types.HikariDictMessage]], Coroutine[None, None, hikari.Message]],
    e: str | Exception = '',
    embed_color: int = S.EMBED_COLORS['error'],
    flags=hikari.MessageFlag.EPHEMERAL,
    **responder_kwargs,
  ):
    if not e:
      e = 'No further information provided'
    responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)
    return await responder(
      embed('An error occured' if isinstance(e, str) else tcr.extract_error(e), e if isinstance(e, str) else tcrd.codeblock(tcr.extract_traceback(e), langcode='py'), color=embed_color),
      flags=flags,
      **responder_kwargs,
    )

  async def text_errpond(
    ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent | Callable[[Unpack[tcrd.types.HikariDictMessage]], Coroutine[None, None, hikari.Message]],
    title: str,
    description: str = 'No further information provided',
    embed_callable: Callable = EMBED.generic_text_error,
    flags=hikari.MessageFlag.EPHEMERAL,
    **responder_kwargs,
  ):
    responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)

    return await responder(embed_callable(title, description), flags=flags, **responder_kwargs)

  async def debugpond(
    ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent | Callable[[Unpack[tcrd.types.HikariDictMessage]], Coroutine[None, None, hikari.Message]],
    obj: Any,
    flags=hikari.MessageFlag.EPHEMERAL,
    **responder_kwargs,
  ):
    responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)
    return await responder(tcrd.codeblock(tcr.fmt_iterable(obj), langcode='py'), flags=flags, **responder_kwargs)

  async def respond_with_attachments_safely(ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent | tcrd.types.HikariResponder, *args, **kwargs) -> tuple[bool, hikari.Message]:
    """True == Success; False == Attachments failed to attach; error raised == Something else happened, not related to attachments."""
    responder = tcr.getattr_queue(ctx, 'respond', 'message.respond', default=ctx)
    try:
      message = await responder(*args, **kwargs)
    except hikari.HTTPError as e:
      if '[getaddrinfo failed]' in e.message:
        return (False, None)
      else:
        raise
    else:
      return (True, message)

  async def respond_with_attachments_or_send_urls_as_file(ctx: arc.GatewayContext | hikari.GuildMessageCreateEvent | tcrd.types.HikariResponder, *args, **kwargs) -> hikari.Message:
    success, message = await respond_with_attachments_safely(ctx, *args, **kwargs)

    if success:
      return message
    else:
      attachments = [kwargs.get('attachment')] if 'attachment' in kwargs else kwargs.get('attachments', [])
      attachments = [att.url for att in attachments if hasattr(att, 'url')]

      kwargs.pop('attachments', None)

      s = 'It looks like your attachments failed to load, here are their URLs:\n'
      s += '\n'.join([f'- {x}' for x in attachments])

      kwargs['attachment'] = hikari.Bytes(s.encode('utf-8'), 'attachment_urls.txt')

      return await respond_with_attachments_safely(ctx, *args, **kwargs)

  def event_uncaught_error_handler_decorator(func: Callable):
    @wraps(func)
    async def wrapper(event: hikari.DMMessageCreateEvent, *args, **kwargs):
      try:
        return await func(event, *args, **kwargs)
      except Exception as e:
        if S.DEV_ERROR_CHANNEL:
          msg = f'## Unhandled command error in `{event.__class__.__name__}` triggered by {tcrd.IFYs.userify(event.author.id)}\n' + tcrd.codeblocks(
            tcr.extract_error(e),
            tcr.extract_traceback(e),
            langcodes=('py', 'py'),
            max_length=tcrd.DiscordLimits.Message.LENGTH_SAFEST,
          )

          await BOT.rest.create_message(S.DEV_ERROR_CHANNEL, msg)

        await event.message.respond(somehow_you_managed_to(f'break the `{event.__class__.__name__}` event handler'), flags=hikari.MessageFlag.EPHEMERAL)

        raw_msg = f'Unhandled event error in {event.__class__.__name__!r} triggered by {event.author.id}'
        c.error(raw_msg)

        if TESTMODE:
          traceback.print_exception(type(e), e, e.__traceback__)

    return wrapper


if True:  # Uncaught error handling

  @ACL.set_error_handler
  async def _cmd_uncaught_error_handler(ctx: arc.GatewayContext, e: Exception):
    if S.DEV_ERROR_CHANNEL:
      msg = f'## Unhandled command error in `{ctx.command.display_name}` triggered by {tcrd.IFYs.userify(ctx.author.id)}\n' + tcrd.codeblocks(
        tcr.extract_error(e),
        tcr.extract_traceback(e),
        langcodes=('py', 'py'),
        max_length=tcrd.DiscordLimits.Message.LENGTH_SAFEST,
      )

      await BOT.rest.create_message(S.DEV_ERROR_CHANNEL, msg)

    await ctx.respond(somehow_you_managed_to(f'break the `{ctx.command.display_name}` command'), flags=hikari.MessageFlag.EPHEMERAL)

    raw_msg = f'Unhandled command error in {ctx.command.display_name!r} triggered by {ctx.author.id}'
    c.error(raw_msg)

    if TESTMODE:
      traceback.print_exception(type(e), e, e.__traceback__)

  @MCL.set_unhandled_component_interaction_hook
  async def _uncaught_component_error_handler(inter: hikari.ComponentInteraction):
    await inter.create_initial_response(
      hikari.ResponseType.MESSAGE_CREATE,
      f'{S.NO} Something went wrong with servicing this request. If this is an old message, please try spawning a new one with appropriate command (for example try spawning the list of reminders again with `.`).',
      flags=hikari.MessageFlag.EPHEMERAL,
    )
    await inter.message.edit(components=[])
