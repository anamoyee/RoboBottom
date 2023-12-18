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
    await channel.send(f"### <@{user_id}>" if ping_user else hikari.UNDEFINED, embed=embed(
      "🔔 Reminder!",
      text[:3950] or 'Uh.. text=None / text=\'\'? Report this bug pls',
      color='#ffff00',
      footer=(S.TOO_LATE_MESSAGE % seconds_to_timestr(too_late)) if too_late else None,
    ), user_mentions=[user_id] if ping_user else hikari.UNDEFINED)

  async def reminder_scheduler(content, responder, author_id, *, force_ephemeral=False, reply_to=hikari.UNDEFINED):
    message_flags = hikari.MessageFlag.NONE if not force_ephemeral else hikari.MessageFlag.EPHEMERAL
    message_flags = message_flags | hikari.MessageFlag.SUPPRESS_NOTIFICATIONS # @silent

    flags, content = separate_flags_from_rest(content)

    # if not is_valid_reminder_syntax(content):
    #   await responder(EMBEDS.invalid_syntax_small(), flags=message_flags, reply=reply_to)
    #   return

    if ' ' not in content:
      await responder(EMBEDS.invalid_syntax_small(), flags=message_flags, reply=reply_to)
      return

    unix, text = content.split(' ', maxsplit=1)
    unix = unix.lower()
    try:
      unix = timestr.to_int(unix)
    except (ValueError, TCRError.ConfigurationError) as e:
      await responder(EMBEDS.invalid_syntax_small(e), flags=message_flags, reply=reply_to)
    else:
      if ((not testmode()) and (unix < S.LIMITS.MINIMAL_DURATION)) or unix < 2:
        await responder(f':x: That\'s too soon! Make sure the delay is at least `{S.LIMITS.MINIMAL_DURATION if not testmode() else 2}` seconds long!' + (f" (`{unix}`)" if testmode() else ""), flags=message_flags, reply=reply_to)
        return

      if schedule_reminder(author_id, text=text, unix=math.floor(time.time()+unix), flags=flags):
        await responder(f"🔔 **{random_sure()}** I'll remind you in **{seconds_to_timestr(unix)}**" + (' ;)' if flags & ReminderFlag.HIDDEN else ''), flags=message_flags, reply=reply_to)
      else:
        await responder(f':x: You reached the limit of `{S.LIMITS.REMINDER}` reminders!', flags=message_flags, reply=reply_to)

  async def send_reminder_view(responder: Callable, reminder: Reminder, rem_id):
    # view = VReminder(reminder, rem_id)
    # message = \
    await responder(EMBEDS.reminder(reminder, rem_id))#, components=view.build())
    # await view.start(message)
    # await view.wait()

if True: # \/ Tasks
  @tasks.task(s=1)
  async def reminder_task():
    for user_id, reminders in get_ALL_reminders().items():
      for reminder in reminders:
        if reminder.unix <= time.time():
          await trigger_and_delete_reminder(user_id, reminder, remind)

  if S.OVERRIDE_ACTIVITY_WITH_BATTERY_PERCENTAGE:
    async def update_battery():
      await update_activity(bot, str(get_battery()) + testmode())

    @tasks.task(s=S.BATTERY_UPDATE_INTERVAL_SECONDS, auto_start=True)
    async def battery_update_task():
      await update_battery()

if True: # \/ Slash Commands
  @bot.command
  @lb.command('botstatus', 'View some (partially made up) details about the bot' + testmode())
  @lb.implements(lb.SlashCommand)
  async def cmd_botstatus(ctx: lb.SlashContext):
    await ctx.respond(embed(
      testmode() or Null,
f"""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>
**Version:** {S.VERSION} ({tcr.nth(S.REVOLUTION)} revolution)
**Uptime:** {uptime()}
**Servers:** {GUILD_COUNT} (May not be up to date)
**Python version:** v{sys.version.split()[0]} (Hikari {hikari.__version__})
**Running on:** {S.RUNNING_ON.LINUX if os.name != 'nt' else S.RUNNING_ON.WINDOWS}
**Memory usage:** {420.69}MB/s/√π
**Gearbot's reminders:** suck
"""[1:-1],
      color='#ff8000',
      author=author_dict(bot.get_me()),
      footer='Like, really all credit should go to Colon, I just recreated it\nHeck, even this embed is taken from one of his bots cuz it looked nice...',
    ), flags=hikari.MessageFlag.EPHEMERAL)

  @bot.command
  @lb.option('doasisay', 'Type exactly "Yes, do as I say!" to confirm.', required=True)
  @lb.command('delhistory', 'Delete all (or most) messages in your DM channel with the bot. Be careful with this one!')
  @lb.implements(lb.SlashCommand)
  async def cmd_delhistory(ctx: lb.SlashContext):
    if ctx.guild_id is not None: return await ctx.respond('You may only use this command in DMs', flags=hikari.MessageFlag.EPHEMERAL)
    if ctx.options.doasisay != "Yes, do as I say!": return await ctx.respond("You did not type the phrase correctly, make sure to use this command carefully!")

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
    ephemeral        = ctx.options.ephemeral if ctx.options.ephemeral is not None else True

    async def r(*args, force_ephemeral=False, **kwargs):
      if ephemeral or force_ephemeral: kwargs['flags'] = hikari.MessageFlag.EPHEMERAL
      await ctx.respond(*args, **kwargs)

    try:
      if thing[0] in ['0', 'devlist', 'list', '-1']:
        await r("""
```md
1. Update guild counter
2. Delete bot's message with syntax: 1.channelID.messageID (deprecated)
3. Get info about guilds the bot is in
4. Get all active reminders
5. Set activity text of the bot
6. Send a fake reminder, syntax: `6.userid.message`
```
"""[1:-1], force_ephemeral=True)
      elif thing[0] in ['1', 'guilds']:
        global GUILD_COUNT
        GUILD_COUNT = await get_guild_count(bot)
        await r(f'Updated the guild count, new guild count: `{GUILD_COUNT}`')
      elif thing[0] in ['2', 'del']:
        await bot.rest.delete_message(thing[1], thing[2])
        await r(f'Deleted message in <#{thing[1]}>', force_ephemeral=True)
      elif thing[0] in ['3', 'ginfo']:
        guilds: list[hikari.OwnGuild] = await bot.rest.fetch_my_guilds()
        await r(f'```\n{print_iterable({guild.id: {"name": guild.name, "my_permissions": guild.my_permissions.value, "icon_url": (guild.icon_url.url.split("?")[0]) if guild.icon_url is not None else None, "created_at": guild.created_at.strftime("%d/%m/%Y, %H:%M:%S")} for guild in guilds}, raw=True)[:1950]}```')
      elif thing[0] in ['4', 'all']:
        await r(f'```\n{print_iterable(ALL(), raw=True).replace("`", APOSTROPHE)}```')
      elif thing[0] in ['5', 'activity']:
        if len(thing) < 2: thing.append(None)
        activity = thing[1] if thing[1] is not None else S.DEFAULT_ACTIVITY_TEXT
        if not activity:
          await bot.update_presence(activity=None)
          await r('Removed activity')
        else:
          await bot.update_presence(activity=hikari.Activity(name=activity + testmode(), type=hikari.ActivityType.WATCHING))
          await r(f"New activity: `{activity}`")
      elif thing[0] in ['6', 'fakeremind', 'fake_remind']:
        try:
          user_id = thing[1]
          text    = thing[2] or ''
          text = text.replace('\\n', '\n')
          if all(x in string.whitespace for x in text):
            raise ValueError
          user_id = int(user_id)
        except (IndexError, ValueError):
          await r('Invalid syntax! use the following syntax: `6.user_id.text` where user_id is an int and text is a non-whitespace string', force_ephemeral=True)
        else:
          await remind(user_id, text, too_late=0)
          await r(f"Sent a reminder to <@{user_id}>", embed=embed(
            "🔔 Reminder!",
            text[:3950] or 'Uh.. text=None / text=\'\'? Report this bug pls',
            color='#ffff00',
          ))
      # elif ...:
      #  ...
      else:
        msg = "Invalid option"
        raise ValueError(msg)
    except Exception as e:
      await r(EMBEDS.e_generic_error(e), force_ephemeral=True)
      if testmode():
        raise

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
    if ' ' not in content and event.message.type == hikari.MessageType.REPLY and timestr.valid(content):
      if event.message.referenced_message is None:
        await event.message.respond("Invalid message")
        return

      if (event.message.referenced_message.author.id != bot.get_me().id) or \
         (not event.message.referenced_message.embeds) or \
         (event.message.referenced_message.embeds[0].title is None) or \
         ('reminder'    not in event.message.referenced_message.embeds[0].title.lower()) or\
         ('reminders'       in event.message.referenced_message.embeds[0].title.lower()) or\
         ('hidden reminder' in event.message.referenced_message.embeds[0].title.lower()):
        await event.message.respond(EMBEDS.no_reply())
        return

      desc = event.message.referenced_message.embeds[0].description

      if desc.startswith('||') and desc.endswith('||'):
        desc = desc.replace('||', '')

      await reminder_scheduler(content + ' ' + desc, event.message.respond, event.author_id, reply_to=event.message_id)
    else:
      await reminder_scheduler(content, event.message.respond, event.author_id)

  async def r_wipe(event: hikari.DMMessageCreateEvent) -> None:
    async def func(btn: miru.Button, ctx: miru.Context, author_id=event.author_id):
      wipe_reminders(author_id)
      await ctx.edit_response(components=[], embed=EMBEDS.wipe(footer='✅ Cancelled all reminders!'))
    view = VClearConfirm(func=func)
    message = await event.message.respond(EMBEDS.wipe(), components=view.build())
    await view.start(message)
    await view.wait()

  async def r_view(event: hikari.DMMessageCreateEvent, content: str) -> None:
    pattern = r'^v(?:iew)? ([1-9]\d{,4})$'
    user_reminders = get_reminders(event.author_id)
    if not (match := regex.match(pattern, content)):
      await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders), do_what='view'))
      return
    rem_id = match.group(1)
    rem_id = int(rem_id)-1

    try:
      rem = user_reminders[rem_id]
    except IndexError:
      await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders), do_what='view'))
    else:
      await send_reminder_view(event.message.respond, rem, rem_id)

  async def r_cancel(event: hikari.DMMessageCreateEvent, content: str) -> None:
    pattern = r'^c(?:ancel)? ([1-9]\d{,4})$'
    user_reminders = get_reminders(event.author_id)
    if not (match := regex.match(pattern, content)):
      await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders)))
      return
    match = match.group(1)
    choice = int(match)
    if len(user_reminders) < choice:
      await event.message.respond(EMBEDS.invalid_syntax_cancel(n=len(user_reminders)))
      return
    reminder = delete_reminder_by_idx(event.author_id, choice-1)
    await event.message.respond(EMBEDS.cancel_success(reminder), flags=hikari.MessageFlag.SUPPRESS_NOTIFICATIONS)

  async def r_reminders(event: hikari.DMMessageCreateEvent):
    rems = get_reminders(event.author_id) # Returns an iterable of Reminder objects
    if len(rems) <= S.LIMITS.REMINDER_PER_PAGE:
      await event.message.respond(EMBEDS.list_(rems), flags=hikari.MessageFlag.SUPPRESS_NOTIFICATIONS)
    else:
      total_count = 0

      def _get_next_count(n: int):
        nonlocal total_count
        total_count += n
        return total_count-n


      pages = [{
        "embed": EMBEDS.list_(rems_, total_override=len(rems), count_from=_get_next_count(len(rems_))),
      } for i, rems_ in enumerate(batched(rems, S.LIMITS.REMINDER_PER_PAGE, back_to_front=True))]

      await send_paged_message_and_wait(event.message.respond, pages=pages, page=-1)

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
    except Exception:
      await event.message.respond('Unable to delete that message... report this as a bug pls')

if True: # \/ Listeners
  @bot.listen(hikari.DMMessageCreateEvent)
  async def on_dm_message(event: hikari.DMMessageCreateEvent):
    if event.is_bot: return # Don't respond to self

    content = event.content
    content = parse_for_aliases(content, event.message.type == hikari.MessageType.REPLY)
    if content is None: return

    aliases = [x + ' ' for x in ['remindme', 'reminder', 'reminders', 'rem', 're', 'rm']]
    for alias in aliases + ['r!' + x for x in aliases]:
      content = multichar_lstrip(content, alias)

    if content in S.ALIASES.LIST:
      await r_reminders(event)
    elif content in S.ALIASES.WIPE:
      await r_wipe(event)
    elif content.startswith(a := ('cancel ', 'c ')) or content in [x.strip() for x in a]:
      await r_cancel(event, content)
    elif content.startswith(a := ('view ', 'v ')) or content in [x.strip() for x in a]:
      await r_view(event, content)
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
    if S.OVERRIDE_ACTIVITY_WITH_BATTERY_PERCENTAGE:
      await update_battery()

if True: # \/ bot.run()
  status_name = S.DEFAULT_ACTIVITY_TEXT + testmode()
  console.log(f'Status: {status_name} // On the eve of our {tcr.nth(S.REVOLUTION)} revolution...')
  if S.OVERRIDE_ACTIVITY_WITH_BATTERY_PERCENTAGE:
    bot.run()
  else:
    bot.run(status=hikari.Status.ONLINE, activity=hikari.Activity(type=hikari.ActivityType.CUSTOM, name='Used in DMs'))#, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
