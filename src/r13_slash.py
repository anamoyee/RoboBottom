from r12_rcomps import *


async def dev_only_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is not authorised to run this dev command. Notifies user by responding."""
  if ctx.author.id not in S.DEV_IDS:
    await ctx.respond(**RESP.not_dev())
    return arc.HookResult(abort=True)
  return arc.HookResult()


async def bannable_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is banned. Notifies user by responding."""
  if ctx.author.id in GDB['banned']:
    await ctx.respond(**RESP.banned())
    return arc.HookResult(abort=True)
  return arc.HookResult()


async def dms_only_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is not in a DM channel."""
  if ctx.guild_id is not None:
    await ctx.respond(**await RESP.must_use_dms(user_id=ctx.author.id))
    return arc.HookResult(abort=True)
  return arc.HookResult()


def do_as_i_say(func: Callable):
  """Ensures the "Yes, do as I said!" confirmation as a slash cmd argument."""

  @wraps(func)
  async def wrapper(*args, **kwargs):
    if not did_as_i_said(kwargs['doasisay']):
      await args[0].respond(f'{S.NO} You did not type the phrase correctly, make sure to use this command carefully!', flags=hikari.MessageFlag.EPHEMERAL)
      return None
    return await func(*args, **kwargs)

  return wrapper


@ACL.include
@arc.with_hook(bannable_hook)
@arc.slash_command('botstatus', 'View some (partially made up) details about the bot' + testmode())
async def cmd_botstatus(
  ctx: arc.GatewayContext,
) -> None:
  revolution = VDB['revolution']
  await ctx.respond(
    embed(
      testmode(dash=False) or tcr.Null,
      f"""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@{S.CREATED_BY['id']}> (@{S.CREATED_BY['name']})
**Version:** `{VERSION}`{f", on the {tcr.nth(revolution)} revolution{' (nice)' if revolution == 69 else ''}"}
**Uptime:** `{UPTIME!s}`
**Servers:** `{await get_guild_count()}` (not be up to date)
**Python version:** `{sys.version.split()[0]}` (hikari `{hikari.__version__}`)
**Running on:** {'windows' if os.name == 'nt' else 'not windows'}
**Memory usage:** `{420.69}MB/s/√π ± {str(2j).replace('j', 'i')}`
**Gearbot's reminders:** suck
"""[1:-1],
      color=S.EMBED_COLORS['colon'],
      author=author_dict(),
      footer='Like, really all credit should go to Colon, I just recreated it\nHeck, even this embed is taken from one of his bots cuz it looked nice...',
    ),
    flags=hikari.MessageFlag.EPHEMERAL,
  )


@ACL.include
@arc.with_hook(bannable_hook)
@arc.slash_command('remind', 'Set a reminder!' + testmode())
async def cmd_remind(
  ctx: arc.GatewayContext,
  reminder: arc.Option[str, arc.StrParams('The reminder (use /help for help)', min_length=1, max_length=418)],
):
  await r_remind(ctx.respond, reminder, user=ctx.author.id, ctx_or_event=ctx)


if True:  # /privacy <...>
  GROUP_PRIVACY = ACL.include_slash_group('privacy', 'Privacy related commands (some dangerous/data-deleting!)' + testmode())
  GROUP_PRIVACY.add_hook(dms_only_hook)

  DOASISAY_OPTION = arc.Option[str, arc.StrParams('Type exactly "Yes, do as I say!" to confirm this potentially dangerous action', min_length=17, max_length=17)]

  @GROUP_PRIVACY.include
  @arc.slash_subcommand('purge', 'PURGE ALL MESSAGES IN THIS DM CHANNEL (DANGEROUS!)' + testmode())
  @do_as_i_say
  async def cmd_privacy_purge(
    ctx: arc.GatewayContext,
    doasisay: DOASISAY_OPTION,
    limit: arc.Option[int, arc.IntParams('Maximum number of messages to delete [1-1000] (1000 by default)', min=1, max=1000)] = 1000,
  ):
    await ctx.respond(f"{S.YES} Deleting messages... (there 's no going back now!)", flags=hikari.MessageFlag.EPHEMERAL)

    messages = await BOT.rest.fetch_messages(ctx.channel_id)
    total = 0
    my_id = BOT.get_me().id
    for message in messages:
      if total >= limit:
        break

      if message.author.id == my_id:
        try:
          await message.delete()
        except hikari.NotFoundError:
          pass
        else:
          total += 1
          await asyncio.sleep(2.5)

    confirmation_message_deleted_in_seconds = tcr.clamp(60, total * 3, 900)
    confirmation_message = await ctx.respond(f'Deleted `{total}` message{tcr.plural_s(total)}.\nThis message will be deleted in {TIMESTR.to_str(confirmation_message_deleted_in_seconds)}...')
    await asyncio.sleep(confirmation_message_deleted_in_seconds)
    with contextlib.suppress(hikari.NotFoundError):
      await confirmation_message.delete()

  @GROUP_PRIVACY.include
  @arc.slash_subcommand('wipe', 'Wipe ALL or PART OF DATABASE associated with your discord ID. (DANGEROUS!)' + testmode())
  @do_as_i_say
  async def cmd_privacy_wipe(
    ctx: arc.GatewayContext,
    doasisay: DOASISAY_OPTION,
    part: arc.Option[str, arc.StrParams('Part of the database to wipe', choices=['EVERYTHING', 'reminders'])] = None,
  ):
    db: U = Database(ctx.author.id)

    match part:
      case 'EVERYTHING':
        db.drop_db()
      case 'reminders':
        db['r'] = U.defaults['r']()
        db['archive'] = U.defaults['archive']()

    await ctx.respond(
      f'{S.YES} Done! You might want to also clean up your discord message history with {get_slash_command_mentions().mentions_named()["privacy purge"]}', flags=hikari.MessageFlag.EPHEMERAL
    )


if True:  # /backup <...>
  GROUP_BACKUP = ACL.include_slash_group('backup', 'Backup your data' + testmode(), autodefer=arc.AutodeferMode.EPHEMERAL)
  GROUP_BACKUP.add_hook(bannable_hook)
  GROUP_BACKUP.add_hook(dms_only_hook)

  @GROUP_BACKUP.include
  @arc.slash_subcommand('export', 'Download your data as a file.' + testmode())
  async def cmd_backup_export(ctx: arc.GatewayContext):
    db: U = Database(ctx.author.id)

    now_unix = int(time.time())
    can_take_backup_on = db['last_taken_backup'] + S.USER_BACKUP_COOLDOWN

    if can_take_backup_on > now_unix:
      await ctx.respond(
        f"{S.NO} You can only take one backup per {TIMESTR.to_str(S.USER_BACKUP_COOLDOWN)}. You can take next backup {tcr.discord.IFYs.timeify(can_take_backup_on, style='R')}",
        flags=hikari.MessageFlag.EPHEMERAL,
      )
      return

    db['last_taken_backup'] = now_unix

    reminders_with_nones = [rem.export() for rem in db['r']]

    exported_data: ExportedDataTD = {
      'settings': db['settings'].export(),
      'reminders': [x for x in reminders_with_nones if x is not None],
    }

    filename = S.USER_BACKUP_EXPORT_FILENAME.format(author_id=ctx.author.id, datetime=datetime.datetime.now(), author_username=ctx.author.username)
    attachment = hikari.files.Bytes(json.dumps(exported_data, indent=2).encode('utf-8'), filename)

    content = f"Here's your backup as a JSON file. You might need to ask an administrator to import it back in (use {S.SLASH_COMMAND_MENTIONS['backup import']} for help)."

    if None in reminders_with_nones:
      content += f'\n{S.WARN} You have `#` hidden reminder(s), those will be left out of the backup.'

    if any(rem.attachments for rem in db['r']):
      content += f"\n{S.WARN} You have reminder(s) with attachments, their attachments may be missing due to discord's dumbassness"

    content += f"\n{S.WARN} You may edit the raw data found within the file but you're on your own then. Manual editing is not really supported and may brick your savefile."

    await ctx.respond(content, flags=hikari.MessageFlag.EPHEMERAL, attachment=attachment)

  @GROUP_BACKUP.include
  @arc.slash_subcommand('import', 'Import your data from an export.' + testmode())
  async def cmd_backup_import(
    ctx: arc.GatewayContext,
    file: arc.Option[hikari.Attachment, arc.AttachmentParams('The file to import (The file your or any discord account got from /backup export)')],
    mode: arc.Option[str, arc.StrParams('The mode to use (Applies to reminders only, settings are alwayys overwritten!)', choices=['append', 'overwrite'])] = 'append',
  ):
    if ctx.author.id not in S.DEV_IDS:
      await ctx.respond('Please contact a developer so they can import your data (WORK IN PROGRESS - CHANGE THIS MESSAGE SOMEDAY)', flags=hikari.MessageFlag.EPHEMERAL)

    try:
      obj: ExportedDataTD = json.loads(await file.read())
    except json.JSONDecodeError:
      await ctx.respond(f'{S.NO} The file you provided contains invalid JSON', flags=hikari.MessageFlag.EPHEMERAL)
      return

    if not isinstance(obj, dict):
      await ctx.respond(f'{S.NO} The file you provided contains invalid structure (outermost must be a dict)', flags=hikari.MessageFlag.EPHEMERAL)
      return

    allowed_keys = ExportedDataTD.__annotations__.keys()

    data, leftover = {k: v for k, v in obj.items() if k in allowed_keys}, {k: v for k, v in obj.items() if k not in allowed_keys}

    async def yes_callback(btn: miru.Button, vctx: miru.ViewContext, *, data: ExportedDataTD = data, ctx=ctx, mode=mode):
      if ctx.author.id != vctx.author.id:
        await vctx.respond('# What would you do if someone touched YOUR buttons??', flags=hikari.MessageFlag.EPHEMERAL)
        return

      db: U = Database(ctx.author.id)

      if 'reminders' in data:
        n_added = 0
        n_skipped = 0

        try:
          reminders_parsed = []
          last_i = 0
          for i, rem in enumerate(data['reminders']):
            last_i = i
            parsed = Reminder.from_export(rem, vctx.author.id)
            if parsed.expired():
              n_skipped += 1
            else:
              n_added += 1
              reminders_parsed.append(parsed)
        except ReminderFromExportMismatchedKeysError as e:
          rest = f'\n\nThe issue arised during parsing of reminder idx={last_i}, missing_keys={e.missing!r}, extra_keys={e.extra!r}'

          await vctx.respond(
            f'{S.NO} There was an error parsing your `reminders` (mismatched keys). Make sure the data is valid and contact a developer in case of any issues.' + rest,
            flags=hikari.MessageFlag.EPHEMERAL,
          )
          return
        except (ValueError, TypeError, AttributeError):
          await vctx.respond(f'{S.NO} There was an error parsing your `reminders`. Make sure the data is valid and contact a developer in case of any issues', flags=hikari.MessageFlag.EPHEMERAL)
          return

        if mode == 'overwrite':
          db['r'] = reminders_parsed
        else:
          for rem in reminders_parsed:
            db.append_reminder(rem)

        msg = f'{S.YES if n_added else S.NO} Reminders processed in {mode} mode...\n{n_added} added'
        if n_skipped:
          msg += f', {n_skipped} skipped due to them being in the past'
        msg += '.'

        data.pop('reminders')

        await vctx.respond(msg, flags=hikari.MessageFlag.EPHEMERAL)

      if 'settings' in data:
        try:
          settings = UserSettings(**data['settings'])
        except TypeError:
          await vctx.respond(f'{S.NO} There was an error parsing your `settings`. Make sure the data is valid and contact a developer in case of any issues', flags=hikari.MessageFlag.EPHEMERAL)

        db['settings'] = settings

        data.pop('settings')

        await vctx.respond(f'{S.YES} Settings processed...', flags=hikari.MessageFlag.EPHEMERAL)

      if data:
        await vctx.respond(somehow_you_managed_to('import invalid data'), flags=hikari.MessageFlag.EPHEMERAL)
      else:
        await vctx.respond(f'{S.YES} All done, your data has been imported')

    await tcr.discord.confirm(
      ctx.respond,
      MCL,
      yes_callback=yes_callback,
      no_callback=tcr.avoid,
      responder_kwargs={
        'embed': EMBED.import_confirmer(import_obj=data, mode=mode, invalid_keys=list(leftover.keys())),
      },
    )

# @ACL.include
# @arc.slash_command(
#   'settings',
#   'Manage settings' + testmode(),
# )
# @bannable_command
# async def cmd_settings(
#   ctx: arc.GatewayContext,
# ):
#   if ctx.guild_id is not None:
#     await ctx.respond(**await RESP.must_use_dms(user_id=ctx.author.id))
#     return

#   with shelve.open(get_db('u', ctx.author.id)) as udb:
#     udb.setdefault('settings', UserSettings())

#     def getattrer(key):
#       try:
#         return getattr(udb['settings'], key)
#       except AttributeError:
#         return next(x.default for x in UserSettings.__attrs_attrs__ if x.name == key)

#     pages = [EMBED.user_settings_single(key, getattrer(key)) for key in SETTINGS_PAGE_KEYS]

#   navigator = nav.NavigatorView(pages=pages, items=[x() for x in SETTINGS_NAVBAR_ITEMS])

#   builder = await navigator.build_response_async(MCL)

#   await ctx.respond_with_builder(builder)
#   MCL.start_view(navigator)

if True:  # *dev_only_commands*
  GROUP_DEV = ACL.include_slash_group('dev', 'Developer cmdlets' + testmode(), autodefer=arc.AutodeferMode.EPHEMERAL, guilds=S.DEV_EANBLED_GUILDS)
  GROUP_DEV.add_hook(dev_only_hook)

  @GROUP_DEV.include
  @arc.slash_subcommand('now', 'Trigger a reminder immediately' + testmode())
  async def cmd_dev_now(
    ctx: arc.GatewayContext,
    idx: arc.Option[int, arc.IntParams('The reminder index to trigger')],
    user_id: arc.Option[str, arc.StrParams('User in question')] = None,
  ):
    await rd_dev_now(responder=ctx.respond, user_id=(ctx.author.id if user_id is None else user_id), idx=idx)

  @GROUP_DEV.include
  @arc.slash_subcommand('get', 'Get a reminder as a codeblock' + testmode())
  async def cmd_dev_get(
    ctx: arc.GatewayContext,
    idx: arc.Option[int, arc.IntParams('The reminder index to get')],
    user_id: arc.Option[str, arc.StrParams('User in question')] = None,
  ):
    await rd_dev_get(responder=ctx.respond, user_id=(ctx.author.id if user_id is None else user_id), idx=idx)

  @GROUP_DEV.include
  @arc.slash_subcommand('guilds', 'Fetch the current guild count & update it.' + testmode())
  async def cmd_dev_guilds(ctx: arc.GatewayContext):
    await rd_dev_guilds(responder=ctx.respond)

  @GROUP_DEV.include
  @arc.slash_subcommand('users', 'Show the current amount of users in the database & list their IDs.' + testmode())
  async def cmd_dev_users(ctx: arc.GatewayContext):
    await rd_dev_users(responder=ctx.respond)

  @GROUP_DEV.include
  @arc.slash_subcommand('run', 'Run a py cmd' + testmode())
  async def cmd_dev_run(
    ctx: arc.GatewayContext,
    code: arc.Option[str, arc.StrParams('The code to run')],
    do_await: arc.Option[bool, arc.BoolParams('await the result if prompted to?', name='await')] = True,
    do_exec: arc.Option[bool, arc.BoolParams('use exec() instead of eval(). retval = _', name='exec')] = False,
  ):
    await rd_run(ctx.respond, code, do_await=do_await, do_exec=do_exec)

  @GROUP_DEV.include
  @arc.slash_subcommand('runfile', 'Run a py file' + testmode())
  async def cmd_dev_runfile(
    ctx: arc.GatewayContext,
    file: arc.Option[hikari.Attachment, arc.AttachmentParams('The file to run (utf-8)')],
    do_await: arc.Option[bool, arc.BoolParams('await the result if prompted to?', name='await')] = True,
    do_exec: arc.Option[bool, arc.BoolParams('use exec() instead of eval(). retval = _', name='exec')] = True,
  ):
    code = await file.read()
    try:
      code = code.decode('utf-8')
    except UnicodeDecodeError:
      await errpond(ctx, 'File must be UTF-8 encoded')
      return

    await rd_run(ctx.respond, code, do_await=do_await, do_exec=do_exec)

  @GROUP_DEV.include
  @arc.slash_subcommand('dbdump', 'Dump database' + testmode())
  async def cmd_dev_dbdump(
    ctx: arc.GatewayContext,
    db: arc.Option[str, arc.StrParams('Database to dump (g, v, u.id)')],
    asfile: arc.Option[bool, arc.BoolParams('Dump as file vs as codeblock')] = False,
    action: arc.Option[str, arc.StrParams('Action to take on the DB.', choices=('show', 'drop'))] = 'show',
    ephemeral: arc.Option[bool, arc.BoolParams('send as ephemeral?')] = True,
  ):
    flags = hikari.MessageFlag.EPHEMERAL if ephemeral else hikari.MessageFlag.NONE

    if not regex.match(r'^g|u|v|(?:u\.[0-9]+)$', db):
      await errpond(ctx, 'Usage: `/dbdump g OR v OR u.<userid>`')
      return

    dbparts = db.split('.')
    if dbparts[0] == 'g':
      outdb = GDB
    elif dbparts[0] == 'v':
      outdb = VDB
    elif dbparts[0] == 'u':
      outdb = Database(dbparts[1] if len(dbparts) > 1 else ctx.author.id)
    else:
      await errpond(ctx, f'Unknown database: `{dbparts[0]!r}`')
      return

    match action:
      case 'show':
        text = tcr.fmt_iterable(outdb)

        if asfile:
          path = tcr.temp_file(text)
          file = hikari.File(path, filename=f'DBDUMP-{db}.txt')
          await ctx.respond(file, flags=flags)
          path.unlink(missing_ok=True)
        else:
          out = tcr.codeblocks(f'Dump of database {db}', text, langcodes=('txt', 'py'))
          await ctx.respond(out, flags=flags)
      case 'drop':
        outdb.drop_db()
        await ctx.respond(f'Dropped db `{db}`', flags=flags)

  @GROUP_DEV.include
  @arc.slash_subcommand('ban', 'Ban or unban a user' + testmode())
  async def cmd_dev_ban(
    ctx: arc.GatewayContext,
    user: arc.Option[str, arc.StrParams('The User ID to ban')],
    unban: arc.Option[bool, arc.BoolParams('Unban the user instead?')] = False,
    drop_db: arc.Option[bool, arc.BoolParams("DANGEROUS: Wipe the banned user's database?")] = False,
  ):
    await rd_ban(ctx.respond, admin_id=ctx.author.id, user=user, unban=unban, drop_db=drop_db)

  @GROUP_DEV.include
  @arc.slash_subcommand('banlist', 'Show all banned users' + testmode())
  async def cmd_dev_banlist(ctx: arc.GatewayContext):
    banned = GDB['banned']

    text = '# Banned Users\n'

    if banned:
      text += '\n'.join(f'- {tcr.discord.IFYs.userify(x)} (`{x}`)' for x in banned)
    else:
      text += 'There are no banned users yet!'

    await ctx.respond(tcr.cut_at(text, tcr.discord.DiscordLimits.Message.LENGTH_SAFE), flags=hikari.MessageFlag.EPHEMERAL)

  @GROUP_DEV.include
  @arc.slash_subcommand('shutdown', 'Shut down the bot' + testmode())
  async def cmd_dev_shutdown(
    ctx: arc.GatewayContext,
    method: arc.Option[str, arc.StrParams('The method of shutdown', choices=('await BOT.close()', 'exit()', 'os._exit(0)'))] = 'await BOT.close()',
  ):
    methods = {
      'await BOT.close()': (BOT.close, True),
      'exit()': (exit, False),
      'os._exit(0)': (lambda: os._exit(0), False),
    }

    func, should_await = methods[method]

    await ctx.respond(f'Shutting down via `{method!s}`...', flags=hikari.MessageFlag.EPHEMERAL)

    if should_await:
      await func()
    else:
      func()

  ERR_MAP = tcr.modules_error_map(builtins, hikari, arc, miru)

  async def autocomplete_dev_error(data: arc.AutocompleteData) -> list[str]:
    text = data.focused_option.value or ''
    text = text.lower()

    def sortkey(x: str) -> tuple:
      dotted_x: str = f'.{x}' if '.' not in x else x
      mod_name, exc_name = dotted_x.split('.', maxsplit=1)
      mod_name, exc_name = mod_name.lower(), exc_name.lower()

      return (
        mod_name,
        -exc_name.startswith(text),
        -mod_name.startswith(text),
        exc_name,
        len(x),
      )

    filtered = filter(lambda x: text in x.lower(), ERR_MAP.keys())
    sorted_ = sorted(filtered, key=sortkey)

    return list(sorted_)[:25]

  @GROUP_DEV.include
  @arc.slash_subcommand('error', "Raise a (to-be-uncaught) exception in order to test the bot's error handling." + testmode())
  async def cmd_dev_error(
    ctx: arc.GatewayContext,
    msg: arc.Option[str, arc.StrParams('The error message')] = None,
    error: arc.Option[str, arc.StrParams('The error type', autocomplete_with=autocomplete_dev_error)] = 'RuntimeError',
  ):
    this_err_map = {x.lower(): y for x, y in ERR_MAP.items()}

    if error.lower() not in this_err_map:
      await ctx.respond(f'{S.NO} Invalid error type: `{tcr.discord.remove_markdown(error)}`', flags=hikari.MessageFlag.EPHEMERAL)

    e = this_err_map[error.lower()]

    if e in (SystemExit, KeyboardInterrupt):
      await ctx.respond(f'{S.WARN} The error you chose (`{e.__name__!s}`) will cause the bot to shut down...', flags=hikari.MessageFlag.EPHEMERAL)

    raise (e(msg) if msg is not None else e)

  @GROUP_DEV.include
  @arc.slash_subcommand('breakpoint', 'Invoke a (synchronous) breakpoint in the bot process.' + testmode())
  async def cmd_dev_breakpoint(
    ctx: arc.GatewayContext,
    type: arc.Option[str, arc.StrParams('The type of breakpoint', choices=('tcr.breakpoint()', 'built-in breakpoint()'))] = 'tcr.breakpoint()',
  ):
    await ctx.respond('Triggering a breakpoint.')

    match type:
      case 'tcr.breakpoint()':
        tcr.breakpoint()
      case 'built-in breakpoint()':
        breakpoint()

  @GROUP_DEV.include
  @arc.slash_subcommand('debug', 'Debug' + testmode())
  async def cmd_dev_debug(
    ctx: arc.GatewayContext,
  ):
    await debugpond(ctx, None, flags=hikari.MessageFlag.EPHEMERAL)
