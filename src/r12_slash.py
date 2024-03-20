from r11_rcomps import *


def dev_only_cmd(func: Callable):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    if args[0].author.id not in S.DEV_IDS:
      return await args[0].respond(**RESP.not_dev())
    return await func(*args, **kwargs)

  return wrapper


@ACL.include
@arc.slash_command(
  'botstatus',
  'View some (partially made up) details about the bot' + testmode(),
)
async def cmd_botstatus(
  ctx: arc.GatewayContext,
) -> None:
  await ctx.respond(
    embed(
      testmode(dash=False) or tcr.Null,
      f"""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>
**Version:** {VERSION}{f", {tcr.nth(REVOLUTION)} revolution {'(nice)' if REVOLUTION == 69 else ''}" if REVOLUTION != -1 else ""}
**Uptime:** {UPTIME!s}
**Servers:** {GUILD_COUNT if GUILD_COUNT != -1 else "<Not fetched yet>"}{' (May not be up to date)' if GUILD_COUNT != -1 else ''}
**Python version:** v{sys.version.split()[0]} (Hikari {hikari.__version__})
**Running on:** {"Windows" if os.name == 'nt' else 'Other than windows (prob 24/7 server)'}
**Memory usage:** {420.69}MB/s/√π
**Gearbot's reminders:** suck
"""[1:-1],
      color=S.EMBED_COLORS['colon'],
      author=author_dict(),
      footer='Like, really all credit should go to Colon, I just recreated it\nHeck, even this embed is taken from one of his bots cuz it looked nice...',
    ),
    flags=hikari.MessageFlag.EPHEMERAL,
  )


@ACL.include
@arc.slash_command(
  'dbdump',
  'Manage databases' + testmode(),
  guilds=S.DEV_EANBLED_GUILDS or hikari.UNDEFINED,
)
@dev_only_cmd
async def cmd_dbdump(
  ctx: arc.GatewayContext,
  db: arc.Option[str, arc.StrParams('Selected database', choices=['users', 'version', 'global'])] = 'users',
  id: arc.Option[int, arc.IntParams('User ID (ignored on non-user db)')] = None,
  user: arc.Option[hikari.User, arc.UserParams('ID from user mention (ignored on non-user db)')] = None,
  file: arc.Option[bool, arc.BoolParams('Whether to dump to a file and send it as an attachment')] = False,
) -> None:
  if db == 'users' and id is None:
    if user is None:  # noqa: SIM108
      id = ctx.author.id
    else:
      id = user.id

  if not tcr.discord.is_snowflake(id):
    return await errpond(ctx)

  db_path = get_db(
    {
      'users': 'u',
      'version': 'v',
      'global': 'g',
    }[db],
    id if db == 'users' else None,
  )

  if db == 'users':
    try:
      user = await BOT.rest.fetch_user(id)
    except (hikari.NotFoundError, hikari.BadRequestError):
      author = None
    else:
      author = author_dict(user)
  else:
    author = None

  with shelve.open(db_path) as shelf:
    formatted = tcr.fmt_iterable(shelf, syntax_highlighting=False)

    if file or len(formatted) > (tcr.DiscordLimits.Embed.DESCRIPTION - 96):
      tempfile = S.DB_DIRECTORY / (f'dbdump-global.txt' if db == 'global' else (f'dbdump-users-{id}.txt' if db == 'users' else f"dbdump-version-{VERSION.replace('.', '_')}.txt"))
      with tempfile.open('w', encoding='utf-8') as f:
        f.write(formatted)

      try:
        await ctx.respond(
          'Contents too large to send as text. Sending as attachment...' if not file else 'Sending as attachment...',
          attachment=hikari.File(tempfile),
          flags=hikari.MessageFlag.EPHEMERAL,
        )
      finally:
        tempfile.unlink()
    else:
      await ctx.respond(
        embed(
          f'Dumping {db} db' + (f' (id={id!r})' if db == 'users' else (f' (VERSION={VERSION!r})' if db == 'version' else '')),
          tcr.codeblock(formatted, langcode='py'),
          author=author,
          color=S.EMBED_COLORS['secondary'],
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
      )


@ACL.include
@arc.slash_command(
  'remind',
  'Set a reminder!' + testmode(),
)
async def cmd_remind(
  ctx: arc.GatewayContext,
  reminder: arc.Option[str, arc.StrParams('The reminder syntax (use /help for help)', min_length=1, max_length=418)],
):
  if ctx.guild_id is not None:
    return await ctx.respond(**await RESP.must_use_dms(user_id=ctx.author.id))

  await r_reminder(ctx.respond, ctx.author.id, reminder)


@ACL.include
@arc.slash_command(
  'settings',
  'Manage settings' + testmode(),
)
async def cmd_settings(
  ctx: arc.GatewayContext,
):
  if ctx.guild_id is not None:
    await ctx.respond(**await RESP.must_use_dms(user_id=ctx.author.id))
    return

  with shelve.open(get_db('u', ctx.author.id)) as udb:
    udb.setdefault('s', UserSettings())

    def getattrer(key):
      try:
        return getattr(udb['s'], key)
      except AttributeError:
        return next(x.default for x in UserSettings.__attrs_attrs__ if x.name == key)

    pages = [EMBED.user_settings_single(key, getattrer(key)) for key in SETTINGS_PAGE_KEYS]

  navigator = nav.NavigatorView(pages=pages, items=[x() for x in S.SETTINGS_NAVBAR_ITEMS])

  builder = await navigator.build_response_async(MCL)

  await ctx.respond_with_builder(builder)
  MCL.start_view(navigator)
