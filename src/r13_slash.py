import hikari.locales
from r12_rcomps import *


def dev_only_cmd(func: Callable):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    if args[0].author.id not in S.DEV_IDS:
      return await args[0].respond(**RESP.not_dev())
    return await func(*args, **kwargs)

  return wrapper


@ACL.include
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
@arc.slash_command('remind', 'Set a reminder!' + testmode())
async def cmd_remind(
  ctx: arc.GatewayContext,
  reminder: arc.Option[str, arc.StrParams('The reminder (use /help for help)', min_length=1, max_length=418)],
):
  await r_remind(ctx.respond, reminder, user=ctx.author.id, ctx_or_event=ctx)


# @ACL.include
# @arc.slash_command(
#   'settings',
#   'Manage settings' + testmode(),
# )
# async def cmd_settings(
#   ctx: arc.GatewayContext,
# ):
#   if ctx.guild_id is not None:
#     await ctx.respond(**await RESP.must_use_dms(user_id=ctx.author.id))
#     return

#   with shelve.open(get_db('u', ctx.author.id)) as udb:
#     udb.setdefault('s', UserSettings())

#     def getattrer(key):
#       try:
#         return getattr(udb['s'], key)
#       except AttributeError:
#         return next(x.default for x in UserSettings.__attrs_attrs__ if x.name == key)

#     pages = [EMBED.user_settings_single(key, getattrer(key)) for key in SETTINGS_PAGE_KEYS]

#   navigator = nav.NavigatorView(pages=pages, items=[x() for x in S.SETTINGS_NAVBAR_ITEMS])

#   builder = await navigator.build_response_async(MCL)

#   await ctx.respond_with_builder(builder)
#   MCL.start_view(navigator)


@ACL.include
@arc.slash_command('debug', 'Debug' + testmode(), guilds=S.DEV_EANBLED_GUILDS)
@dev_only_cmd
async def cmd_debug(
  ctx: arc.GatewayContext,
):
  # await debugpond(ctx, 'Nothing to debug')
  await debugpond(ctx, 'Nothing to debug')


@ACL.include
@arc.slash_command(
  'run', 'Run a py cmd' + testmode(), name_localizations={hikari.Locale.PL: 'biegać'}, description_localizations={hikari.Locale.PL: 'Zabiegaj cmd py' + testmode()}, guilds=S.DEV_EANBLED_GUILDS
)
@dev_only_cmd
async def cmd_run(
  ctx: arc.GatewayContext,
  code: arc.Option[str, arc.StrParams('The code to run', name_localizations={hikari.Locale.PL: 'kot'}, description_localizations={hikari.Locale.PL: 'Kot do zabiegania'})] = None,
  file: arc.Option[
    hikari.Attachment, arc.AttachmentParams('The file to run', name_localizations={hikari.Locale.PL: 'pilnik'}, description_localizations={hikari.Locale.PL: 'Pilnik do zabiegania'})
  ] = None,
  do_await: arc.Option[
    bool, arc.BoolParams('await the result if prompted to?', name='await', name_localizations={hikari.Locale.PL: 'zaczekaj'}, description_localizations={hikari.Locale.PL: 'Zaczekaj na rezultat'})
  ] = True,
  do_exec: arc.Option[
    bool,
    arc.BoolParams(
      'use exec() instead of eval(). retval = _', name='exec', name_localizations={hikari.Locale.PL: 'wykonaj'}, description_localizations={hikari.Locale.PL: 'Wykonaj zamiast oceń'}
    ),
  ] = None,
):
  if code is None and file is None:
    await errpond(ctx, 'Exactly one of `code` or `file` is required')
    return

  if code is not None and file is not None:
    await errpond(ctx, 'Only one of `code` or `file` is allowed')
    return

  if do_exec is None:
    do_exec = file is not None  # exec is by default True if file is supplied

  if file:
    code = await file.read()
    try:
      code = code.decode('utf-8')
    except UnicodeDecodeError:
      await errpond(ctx, 'File must be UTF-8 encoded')
      return

  await rd_run(ctx.respond, code, do_await=do_await, do_exec=do_exec)


@ACL.include
@arc.slash_command('dbdump', 'Dump database' + testmode(), guilds=S.DEV_EANBLED_GUILDS)
@dev_only_cmd
async def cmd_dbdump(
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
