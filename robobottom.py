from imports import *

if True: # \/ BotApp
  bot = lb.BotApp(
    token=TOKEN,
    banner=None,
    default_enabled_guilds=S.DEFAULT_ENABLED_GUILDS,
  )
  miru.install(bot)
  tasks.load(bot)

if True: # \/ Bot-dependant funcs
  async def remind(user_id, text, too_late=1, *, ping_user=False, hide_text=False):
    channel = await bot.rest.create_dm_channel(user_id)
    if text and hide_text:
      text = f'||{text.replace("|", FAKE_PIPE)}||'
    await channel.send(f"<@{user_id}>" if ping_user else hikari.UNDEFINED, embed=embed(
      "🔔 Reminder!",
      text or 'Uh.. text=None / text=\'\'? Report this bug pls',
      color='#ffff00',
      footer=f'Sowwy fow sending thwis wemindeww {seconds_to_timestr(too_late)} too lwate!!! >.<' if too_late else None,
    ), user_mentions=[user_id] if ping_user else hikari.UNDEFINED)

  async def reminder_scheduler(content, responder, author_id, *, force_ephemeral=False):
    message_flags = hikari.MessageFlag.NONE if not force_ephemeral else hikari.MessageFlag.EPHEMERAL
    message_flags = message_flags | hikari.MessageFlag.SUPPRESS_NOTIFICATIONS # @silent

    flags, content = separate_flags_from_rest(content)

    if not is_valid_reminder_syntax(content):
      await responder(EMBEDS.invalid_syntax_small(), flags=message_flags)
      return

    unix, text = content.split(' ', maxsplit=1)
    unix = unix.lower()
    try:
      unix = timestr_to_seconds(unix)
    except ValueError:
      await responder(EMBEDS.invalid_syntax_small(), flags=message_flags)
    else:
      if (not testmode()) and (unix < S.LIMITS.MINIMAL_DURATION):
        await responder(f':x: That\'s too soon! Make sure the delay is at least `{S.LIMITS.MINIMAL_DURATION}` seconds long!', flags=message_flags)
        return

      if schedule_reminder(author_id, text=text, unix=math.floor(time.time()+unix), flags=flags):
        await responder(f"🔔 **{random_sure()}** I'll remind you in **{seconds_to_timestr(unix)}**" + (' ;)' if flags & ReminderFlag.HIDDEN else ''), flags=message_flags)
      else:
        await responder(f':x: You reached the limit of `{S.LIMITS.REMINDER}` reminders!', flags=message_flags)

if True: # \/ Tasks
  @tasks.task(s=1)
  async def reminder_task():
    for user_id, reminders in get_ALL_reminders().items():
      for reminder in reminders:
        if reminder.unix <= time.time():
          await trigger_and_delete_reminder(user_id, reminder, remind)

if True: # \/ Slash Commands
  @bot.command
  @lb.command('botstatus', 'View some (partially made up) details about the bot' + testmode())
  @lb.implements(lb.SlashCommand)
  async def cmd_botstatus(ctx: lb.SlashContext):
    await ctx.respond(embed(
      Null if not USING_TOKEN2 else "Testmode",
f"""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>
**Version:** {S.VERSION}
**Uptime:** {uptime()}
**Servers:** {GUILD_COUNT} (May not be up to date)
**Python version:** v{sys.version.split()[0]} (Hikari {hikari.__version__})
**Running on:** {S.RUNNING_ON.LINUX if os.name != 'nt' else S.RUNNING_ON.WINDOWS}
**Memory usage:** {420.69}MB/s/√π
**Gearbot's reminders:** suck
"""[1:-1],
      color='#ff8000',
      author=author_dict(bot.get_me()),
      footer='Like, really all credit should go to Colon, I just recreated it 1:1\nHeck, even this embed is taken from one of his bots cuz it looked nice...',
    ), flags=hikari.MessageFlag.EPHEMERAL)

  @bot.command
  @lb.command('delhistory', 'Delete all (or most) messages in your DM channel with the bot. Be careful with this one!')
  @lb.implements(lb.SlashCommand)
  async def cmd_delhistory(ctx: lb.SlashContext):
    if ctx.guild_id is not None: await ctx.respond('You may only use this command in DMs', flags=hikari.MessageFlag.EPHEMERAL)

    this_message = await ctx.respond('Deleting messages...')

    messages = await bot.rest.fetch_messages(ctx.channel_id)
    total = 0
    for message in messages:
      if message.author.id == bot.get_me().id and message.id != (await this_message.message()).id:
        try:
          await message.delete()
        except hikari.errors.NotFoundError:
          pass
        else:
          total += 1

    deltime = 5
    try:
      another_message = await ctx.edit_last_response(f'Deleted `{total}` message{"s" if total != 1 else ""}\nThis message will be deleted in {deltime} seconds...')
    except hikari.errors.NotFoundError:
      pass
    else:
      await asyncio.sleep(deltime)
      with contextlib.suppress(hikari.errors.NotFoundError):
        await another_message.delete()

  @bot.command
  @lb.option('section', 'Feature to view specific help on, leave blank to view general help', required=False, choices=HELPMSGS)
  @lb.command('help', 'View bot\'s help page or specific help about certain command' + testmode())
  @lb.implements(lb.SlashCommand)
  async def cmd_help(ctx: lb.SlashContext):
    if ctx.options.section is None:
      await ctx.respond(HELPMSG_NONE, flags=hikari.MessageFlag.EPHEMERAL)
    else:
      await ctx.respond(HELPMSGS[ctx.options.section], flags=hikari.MessageFlag.EPHEMERAL)

  @bot.command
  @lb.option('ephemeral', "Sneaky sneaky (False by default)", type=bool, required=False)
  @lb.option('thing', "The thing to do", required=True)
  @lb.command('dev', 'Do dev stuff!' + testmode(), guilds=[S.DEV_GUILD])
  @lb.implements(lb.SlashCommand)
  async def cmd_dev(ctx: lb.SlashContext):
    if ctx.author.id != S.DEV_ID: return await ctx.respond('You are not allowed to use this command', flags=hikari.MessageFlag.EPHEMERAL)

    thing: list[str] = ctx.options.thing.split('.')
    ephemeral        = ctx.options.ephemeral

    async def r(*args, force_ephemeral=False, **kwargs):
      if ephemeral or force_ephemeral: kwargs['flags'] = hikari.MessageFlag.EPHEMERAL
      await ctx.respond(*args, **kwargs)

    try:
      if thing[0] in ['0', 'guilds']:
        global GUILD_COUNT
        GUILD_COUNT = await get_guild_count(bot)
        await r(f'Updated the guild count, new guild count: `{GUILD_COUNT}`')
      elif thing[0] in ['1', 'del']:
        await bot.rest.delete_message(thing[1], thing[2])
        await r(f'Deleted message in <#{thing[1]}>', force_ephemeral=True)
      elif thing[0] in ['2', 'ginfo']:
        guilds = await bot.rest.fetch_my_guilds()
        await r(f'```\n{print_iterable({guild.id: guild.name for guild in guilds}, raw=True)}```')
      elif thing[0] in ['3', 'all']:
        await r(f'```\n{print_iterable(ALL(), raw=True).replace("`", APOSTROPHE)}```')
      # elif ...:
      #  ...
      else:
        msg = "Invalid option"
        raise ValueError(msg)
    except Exception as e:
      await r(EMBEDS.e_generic_error(e), force_ephemeral=True)

  @bot.command
  @lb.option('ephemeral', "Sneaky sneaky (True by default)", type=bool, required=False)
  @lb.option('code', "The thing to run", required=True)
  @lb.command('run', 'Do even more dev stuff!' + testmode(), guilds=[S.DEV_GUILD])
  @lb.implements(lb.SlashCommand)
  async def cmd_run(ctx: lb.SlashContext):
    if ctx.author.id != S.DEV_ID: return await ctx.respond('You are not allowed to use this command', flags=hikari.MessageFlag.EPHEMERAL)

    code      = ctx.options.code
    ephemeral = ctx.options.ephemeral if ctx.options.ephemeral is not None else True

    async def r(*args, force_ephemeral=False, **kwargs):
      if ephemeral or force_ephemeral: kwargs['flags'] = hikari.MessageFlag.EPHEMERAL
      await ctx.respond(*args, **kwargs)

    try:
      await r(f'```{eval(code)}```')
    except Exception as e:
      await r(EMBEDS.e_generic_error(e), force_ephemeral=True)

  @bot.command
  @lb.option('text',  "The reminder's text",                                                  required=True, min_length=1, max_length=100, type=str)
  @lb.option('delay', "The delay to remind you after, for example 6h56m, see /help for help", required=True, min_length=2, max_length=100, type=str)
  @lb.command('remind', "Set a reminder!" + testmode())
  @lb.implements(lb.SlashCommand)
  async def cmd_remind(ctx: lb.SlashContext):
    content = ctx.options.delay + ' ' + ctx.options.text
    content = content.strip()
    content = parse_for_aliases(content)
    await reminder_scheduler(content, ctx.respond, ctx.author.id, force_ephemeral=bool(ctx.guild_id is not None)) # Force ephemeral on server, such that there's no spam/unnecessary messages, but don't ephemeral in DMs

if True: # \/ Reminder Components
  async def r_schedule(event: hikari.DMMessageCreateEvent, content: str):
    await reminder_scheduler(content, event.message.respond, event.author_id)

  async def r_wipe(event: hikari.DMMessageCreateEvent):
    async def func(btn: miru.Button, ctx: miru.Context, author_id=event.author_id):
      wipe_reminders(author_id)
      await ctx.edit_response(components=[], embed=EMBEDS.wipe(footer='✅ Cancelled all reminders!'))
    view = VClearConfirm(func=func)
    message = await event.message.respond(EMBEDS.wipe(), components=view.build())
    await view.start(message)
    await view.wait()

  async def r_cancel(event: hikari.DMMessageCreateEvent, content: str):
    pattern = r'^cancel ([1-9]\d{,4})$'
    user_reminders = get_reminders(event.author_id)
    if not (match := regex.match(pattern, content)):
      return await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders)))
    match = match.group(1)
    choice = int(match)
    if len(user_reminders) < choice:
      return await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders)))
    reminder = delete_reminder_by_idx(event.author_id, choice-1)
    await event.message.respond(EMBEDS.cancel_success(reminder), flags=hikari.MessageFlag.SUPPRESS_NOTIFICATIONS)

  async def r_reminders(event: hikari.DMMessageCreateEvent):
    rems = get_reminders(event.author_id)
    await event.message.respond(EMBEDS.list_(rems), flags=hikari.MessageFlag.SUPPRESS_NOTIFICATIONS)

  async def r_delete(event: hikari.DMMessageCreateEvent):
    other_message = event.message.referenced_message

    if other_message is None:
      await event.message.respond('Reply to the message you want me to delete!')
      return
    if other_message.author.id != bot.get_me().id:
      await event.message.respond('That\'s not my message, I dont have permission to delete it!')
      return

    try:
      await other_message.delete()
    except Exception as e:
      await event.message.respond('Unable to delete that message... report this as a bug pls')

if True: # \/ Listeners
  @bot.listen(hikari.DMMessageCreateEvent)
  async def on_dm_message(event: hikari.DMMessageCreateEvent):
    if event.is_bot: return # Don't respond to self

    content = event.content
    content = parse_for_aliases(content)
    if content is None: return

    aliases = [x + ' ' for x in ['remindme', 'reminder', 'reminders', 'rem', 're', 'rm']]
    for alias in aliases + ['r!' + x for x in aliases]:
      content = multichar_lstrip(content, alias)

    if content in S.ALIASES.LIST:
      await r_reminders(event)
    elif content in S.ALIASES.WIPE:
      await r_wipe(event)
    elif content.startswith('cancel ') or content == 'cancel':
      await r_cancel(event, content)
    elif content in S.ALIASES.DELETE:
      await r_delete(event)
    else:
      await r_schedule(event, content)

  GUILD_COUNT = 0
  @bot.listen(hikari.StartedEvent)
  async def started_event(event: hikari.StartedEvent):
    global GUILD_COUNT
    GUILD_COUNT = await get_guild_count(bot)
    console.log(f'Guild Count: {GUILD_COUNT}')
    reminder_task.start()

if True: # \/ bot.run()
  status_name = S.STATUS + testmode()
  console.log(f'Status: {status_name}')
  bot.run(status=hikari.Status.ONLINE, activity=hikari.Activity(type=hikari.ActivityType.WATCHING, name=status_name))#, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
  # Temporarly a "watching" status until a get custom statuses to work huh...