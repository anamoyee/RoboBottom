import arc
import hikari
from common.arc import *

if True:  # Plugin boilerplate
  plugin = arc.GatewayPlugin('bar')

  @arc.loader
  def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)

  @arc.unloader
  def unloader(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)


GROUP_HELP = plugin.include_slash_group('help', 'How to use the bot.', autodefer=arc.AutodeferMode.EPHEMERAL)


@GROUP_HELP.include
@arc.with_hook(bannable_hook)
@arc.slash_subcommand('help', 'How to use the bot and this help menu.')
async def cmd_help_help(ctx: arc.GatewayContext):
  em = hikari.Embed(
    title='Basic Help & Usage',
    description=f'Use `/help <section>` with section specified to get more info that part of the bot.',
    color=R.S.EMBED_COLORS['primary'],
  ).add_field(
    name='Usage',
    value=f"""
- You don't need to use the robotop's prefix (`r!`) or any other prefix
  - The bot is mainly used in DMs where `r!remind ` prefix is implied
- It can also be used on servers with slash commands though
- Bot's status and other more or less helpful stats are available with {R.slash_mention('botstatus')}
- View credits with {R.slash_mention('help credits')}
- View detailed usage manual with {R.slash_mention('help usage')}
"""[1:-1],
  )

  await ctx.respond(em, flags=hikari.MessageFlag.EPHEMERAL)

@GROUP_HELP.include
@arc.with_hook(bannable_hook)
@arc.slash_subcommand('credits', 'Credits & Attributions.')
async def cmd_help_credits(ctx: arc.GatewayContext):
  em = hikari.Embed(
    title='Credits & Attributions',
    description="""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>

RoboTop was really such a great bot. Perhaps the greatest i've ever used. After it shut down I really missed the reminders so I remade them! This is __not__ my original idea, most of the looks and functionality is remade to be exactly (or really close to) original **[Colon](https://gdcolon.com)**'s bot and I just made it reminders-only.
"""[1:-1],
    color=R.S.EMBED_COLORS['colon'],
  )

  await ctx.respond(em, flags=hikari.MessageFlag.EPHEMERAL)

@GROUP_HELP.include
@arc.with_hook(bannable_hook)
@arc.slash_subcommand('usage', 'Help with the bot usage.')
async def cmd_help_usage(ctx: arc.GatewayContext):
  em = hikari.Embed(
    title='Reminders usage & syntax',
    description=f"""
### Reminder structure: ||(delay is required, others optional)||
### **`[flags]<delay> [message text]`**

### The reminder is parsed as follows:
1. left-strip and remember any flag characters from the message (if any), until the leftmost character is not a flag, *more about and what are flags later.*
  - ||For example: `!1h IMPORTANT MEETING` -> `!`, `1h IMPORTANT MEETING`||
2. Split the reminder by the first space into `delay` and `message text`.
  - ||For example: `1h praise senko` → `1h`, `praise senko`||
3. Split the reminder `delay` by `!` and evaluate each group separately:
  - ||For example: `1h30m!13:` → [`1h30m`, `13:`]||
  - For each group: resolve any aliases, relative or absolute units & add them up
4. Add up each group delay to get the total delay and set the reminder to expire in that amount of time, then continuously check, **every {(a := (round(R.S.REMINDER_TASK_INTERVAL_SECONDS)))} second{tcr.plural_s(a)}** if the reminder has expired, and if it did deliver it to the user.

"""[1:-1],
    color=R.S.EMBED_COLORS['primary'],
  ).add_field(
    name='Examples',
    value="""
`5h59m rescue                 `
`1h BUY THE GD COLOGNE PLUSHIE`
`3h.5d praise senko           `
"""[1:-1],
    inline=True,
  ).add_field(
    name='Units vs reminder text distinction',
    value="""
`10h50m finish this discord bot`
`^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^`
` time        your message     `
"""[1:-1],
    inline=True,
  ).add_field(
    name='Units',
    value="""
`s`, `sec`, `seconds`
`m`, `min`, `minutes`
`h`, `hr`, `hours`
`w`, `weeks`
`y`, `years`
`pul`, `pull`, `card` alias for `11.5h`
`res`, `rescues` alias for `6h`
`???`, `???????????` (easteregg/hidden reference)
All singular/plural versions of the nouns should be valid as well (secs, mins)
"""[1:-1],
  ).add_field(
    name='Delay groups / time specifiers',
    value=f"""
Any of the listed here groups can be concatenated with each other by the use of the `!` symbol, for example: `14:!1.`
Enhance your reminder-setting experience using any (or multiple) of these specifiers:
- `1h` - Robotop syntax: `<amount><unit>` (works with any unit listed above).
  - Chain them together without splitting into groups: `1d1h1m`
  - Supports negative values: `1h-5m` = `55m`
  - And fractions: `.5h` = `30m`
- `13:` - `ti:me` syntax: Set hour, minute, or second precision time (e.g., `13:`, `13:30`, `13:30:59`). Finds the nearest matching time and allows offsets using `da:te` or robotop syntax. Requires at least one `:` and valid clock-like format.
- `13.` - `da:te` syntax: Similar to `ti:me` but for dates (e.g., `13.`, `13.2`, `13.02`, `13.02.26`, `13.02.2026`). Finds the closest date and adds the delay in full days. Compatible with `ti:me` syntax.
- `mon` - Weekday syntax: Adds full days to reach the specified weekday (`mo`, `mon`, `monday`, `pon`, `poniedziałek`).
"""[1:-1],
  ).add_field(
    name='Aliases',
    value="""
`pul` -> `1pul pul`
`card` -> `1card card`
`rescue` -> `1rescue rescue`
`<anything not containing a space>` -> `<said thing> <said thing>`
^^^ For example `1h` -> `1h 1h`, to fill in the optional `message text`
"""[1:-1]
  ).add_field(
    name='Flags',
    value="""
`!` - **Important**: Will ping you when reminded
`#` - **Hidden**: Will hide the reminder's contents until you're reminded
`&` - **Recurring** - Will re-schedule the reminder after delivering it

**How to use it?** Add one or more flag characters to the beginning of your reminder delay, for example: `!#1h Pet the Colon plushie` ← This reminder now has the **Important** and **Hidden**, but not **Recurring** flags set and will behave as such.
"""[1:-1]
  )

  await ctx.respond(em, flags=hikari.MessageFlag.EPHEMERAL)

@GROUP_HELP.include
@arc.with_hook(bannable_hook)
@arc.slash_subcommand('list', 'Help with viewing the list of your reminders.')
async def cmd_help_list(ctx: arc.GatewayContext):
  em = hikari.Embed(
    title='List command usage.',
    description=f'This is a placeholder text to edit when the list commands gains advanced search ability and stuff...',
    color=R.S.EMBED_COLORS['primary'],
    # TODO: Whenever the mentioned stuff is coded in (the advanced searches and stuff) add help here.
    # TODO: When the archive is finished mention it here too
  ).add_field(
    name='Usage & Example',
    value='`list`, `.`\nThis will be updated once the above stuff is coded in.',
  ).add_field(
    name='Aliases',
    value=', '.join(['`' + x + '`' for x in P.DM_CMD_ALIASES.get_n_shortest('list')]),
  )

  await ctx.respond(em, flags=hikari.MessageFlag.EPHEMERAL)
