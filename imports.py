if True: # \/ Imports
  import datetime
  import math
  import os
  import pathlib as p
  import random as rng
  import re as regex
  import shelve
  import sys
  import time
  import typing as t
  from functools import reduce

  import hikari
  import lightbulb as lb
  import miru
  import pytz
  from colored import attr, bg, fg, stylize
  from lightbulb.ext import tasks

  import settings as S
  from imports import *
  from secrets_ import TOKEN

class Tz:
  def get_localzone(self):
    return pytz.timezone('Europe/Warsaw')
tz = Tz()

if True: # \/ Critical Funcs do not touch
  class Null:
    def __str__(self):
      return ''
    def __repr__(self):
      return 'Null'
  Null = Null()
  def F(item: str) -> str: # Function to convert strings in settings to contain up to date versions of variables (if there's a better way of doing this then idc it works and that's all that matters)
    return eval(f'f{item!r}') # Don't complain pls i really just didn't feel like taking a better (more time consuming) approach to this lol
  def print_iterable(it: list | tuple | dict, *, recursive=True, raw=False) -> str | None: # Required for debugging (console object)
    if it == []:
      return '[]'
    if it == ():
      return '()'
    if it == {}:
      return '{}'
    if isinstance(it, dict):
      text = '{'
      for key, value in it.items():
        if recursive and isinstance(value, list | tuple | dict):
          value = print_iterable(value, raw=True).replace('\n', '\n  ')
        else:
          value = repr(value)
        text += f'\n  {key!r}: {value},'
      text += '\n}'
    else:
      text = '[' if isinstance(it, list) else '('
      for value in it:
        if recursive and isinstance(value, list | tuple | dict):
          value = print_iterable(value, raw=True).replace('\n', '\n  ')
        else:
          value = repr(value)
        text += f'\n  {value},'
      text += '\n]' if isinstance(it, list) else '\n)'

    if raw:
      return text
    print(text)
    return None
  def embed(title: str, description: str, *, url=None, color=None, timestamp=None, thumbnail=None, footer=None, footer_icon=None, author: dict | None=None, image=None, fields: list | None=None) -> hikari.Embed:
    if (title is not Null and not title.strip()) or (description is not Null and not description.strip()):
      msg = f'Both title and description must be non-whitespace-only strings unless explicitly specified the title to be Null, got Title: {title!r}, Description: {description!r}'
      raise ValueError(msg)

    if fields is None:
        fields = []

    if author is None:
        author = {}

    out = hikari.Embed(
                        title=title,
                        description=description,
                        color=color,
                        timestamp=timestamp,
                        url=url,
                      )

    if thumbnail:
      out = out.set_thumbnail(thumbnail)

    if footer:
      out = out.set_footer(text=footer, icon=footer_icon)
    if author:
      out = out.set_author(**author)
    if image:
      out = out.set_image(image)

    for field in fields:
      if len(field) == 2:
        field = (*field, False)
      out = out.add_field(field[0], field[1], inline=field[2])
    return out
  def extract_error(value, pattern='%s: %s', *, raw=False):
    one = repr(value).split('(')[0]
    two = str(value)
    return (one, two) if raw else pattern % (one, two)
  start_time = datetime.datetime.now(tz=tz.get_localzone())

class Console:
  def log     (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                         ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = F('I {str(datetime.datetime.now())[:-3].replace(".", ",")} ') + out
    out = stylize(out, fg("light_green") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def warn    (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                         ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = F('W {str(datetime.datetime.now())[:-3].replace(".", ",")} ') + out
    out = stylize(out, fg("yellow") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def error   (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                         ) -> None or str:
    if not values: values = ['']
    values = [(extract_error(x) if isinstance(x, Exception) else x) for x in values]
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = F('E {str(datetime.datetime.now())[:-3].replace(".", ",")} ') + out
    out = stylize(out, fg("red") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def debug   (self, *values, sep=' ', end='', returnonly=False, withprefix=True, print_iterable_=True, passthrough=False) -> None or str:
    if not values: values = ['']
    if len(values) > 1:
      out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    else:
      out = values[0]
    if isinstance(out, type({}.values()) | type({}.keys())):
      out = list(out)
    if print_iterable_ and isinstance(out, list | tuple | dict):
      out = print_iterable(out, raw=True)
    out = str(out)
    if withprefix:
      out = F('D {str(datetime.datetime.now())[:-3].replace(".", ",")} ') + out
    out = stylize(out, fg("#FF12FF") + attr('bold'))# + attr("underlined"))
    if returnonly:
      return out
    print(out)
    return None if not passthrough else values[0]
  def critical(self, *values, sep=' ', end='', returnonly=False, withprefix=True                                         ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = F('C {str(datetime.datetime.now())[:-3].replace(".", ",")} ') + out
    out = stylize(out, bg("#FF0000") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
console = Console()

NEWLINE = '\n'; APOSTROPHE = '\''
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # noqa: PTH120, PTH100
SHELF_DIRECTORY = p.Path('./db') if os.name == 'nt' else p.Path('./../../RoboBottomDB'); SHELF_DIRECTORY.mkdir(exist_ok=True, parents=True) # When hosting on termux on my phone make the reminders global for all versions that have this line (v1.0.3 and higher)
SYNTAX_REGEX = r'^(?:(?:(?:[1-9]\d*\.\d+)|(?:\.?\d+))[a-zA-Z]+)+ +(?:.|\s){1,100}$'

class Embeds:
  def e_generic_error(self, e: Exception, *, author=None, **kwargs):
    # return embed(*extract_error(e, raw=True), color=0xFF0000, author=author_dict(author), **kwargs)
    return embed(
      *extract_error(e, raw=True),
      color=('#FF8000' if rng.randint(1, 100) == 1 else '#FF0000'),
      footer=(S.OOPSIE_WOOPSIE if rng.randint(1, 100) == 1 else ''),
    ) # Oopsie Woopsie :3

  def invalid_syntax_small(self):
    return embed(
      "Invalid syntax",
      "To view syntax guide use the </help:1146446941278965793> with section set to `Remind`",
      color='#ff0000' if rng.randint(1, 100) != 1 else '#ff8000',
    )
  def invalid_syntax_big(self, _in_help=False):
    return embed(
        'Invalid syntax' if not _in_help else 'Reminders',
        'Provide a delay in the format of at least one `[NUMBER][UNIT]` group or multiple for example `30m` or `1y30w` or `1h.25d` then separate it with a space and provide your message. The message must be between 1 and 100 characters long and must be separated from the delay with a space.\nAdditionally make sure all units are correct',
        fields=[
          ("Examples", "`5h59m rescue                 `\n`1h BUY THE GD COLOGNE PLUSHIE`\n`3h.5d praise senko           `", True),
          ("Uh.. also example", """
`10h50m finish this discord bot`
`^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^`
` time        your message     `
"""[1:-1], True),
          ("Units", "`s`, `sec`, `seconds`\n`m`, `min`, `minutes`\n`h`, `hr`, `hours`\n`w`, `weeks`\n`y`, `years`\n`???`, `???????????` (easteregg/hidden reference)\nAll singular/plural versions of the nouns should be valid as well", False),
        ],
        footer=F'The above regex if you know how regex works (doesn\'t include unit validation):\n/{SYNTAX_REGEX}/g',
        color='#ff0000' if not _in_help else "#00ccff",
      )
  def invalid_syntax_cancel(self, n=99999):
    return embed(
        'Invalid syntax/choice',
       f'Use the following syntax: `cancel <1-{n}>`' if n > 0 else 'You don\'t have any reminders to cancel, therefore every number you choose will result in invalid choice',
        color='#ff0000',
      )
  def cancel_success(self, text):
    return embed(
      'Successfully cancelled a reminder!',
      text,
      color='#00ccff',
    )

  def wipe(self, footer=None):
    return embed(
      'Are you sure?',
      "This will cancel **ALL** your reminders!",
      color=('#ff0000' if rng.randint(1, 100) != '1' else '#ff8000'),
      footer=footer,
    )
  def list_(self, rems, *, who: str | None = None):
    display_rems = '\n'.join([f'{i+1}) **{x.text.replace(NEWLINE, " ")}** (<t:{x.unix}:R>)' for i, x in enumerate(rems)])
    if display_rems: display_rems += '\n\n'
    rest = f"Cancel a reminder with `cancel [1-{len(rems)}]`"
    return embed(
      f"{'Your' if who is None else ((who + APOSTROPHE + 's') if not who.endswith('s') else (who + APOSTROPHE))} reminders ({len(rems)})",
      f'{display_rems}{rest}'.rstrip('\n'),
      color='#00ccff',
    )
EMBEDS = Embeds()

HELPMSGS = {
  'Remind - Syntax':                       EMBEDS.invalid_syntax_big(_in_help=True),
  'List your reminders':          embed(
      "List of reminders",
      "Simple. Shows you the list of reminders.",
      color='#00ccff',
      fields=[
        (
          "Usage & Example",
          "`list`",
          False,
        ),(
          "Aliases",
          ', '.join(['`' + x + '`' for x in S.ALIASES.LIST]),
          False,
        ),
      ],
    ),
  'Cancel a reminder':            embed(
      "Cancelling Reminders",
      "Use the following syntax: `cancel <1-99999>` where you specify the index of the reminder that you want to cancel.\nTo see the list of your reminders along with the indices type `list` or view its help by using </help:1146216876779774012> with section argument `list`",
      color='#00ccff',
      fields=[
        (
          "Usage",
          "Anything that starts with `cancel` is considered a canceling command",
          False,
        ),(
          "Example",
          "`cancel 1`",
          False,
        ),
      ],
    ),
  'Clear (cancel) all reminders': embed(
      "Clearing all reminders",
      "To clear (cancel) all reminders type `clear` (or any of its aliases) and it will remove all of your set reminders without reminding you",
      color='#00ccff',
      fields=[
        (
          "Aliases",
          ', '.join(['`' + x + '`' for x in S.ALIASES.WIPE]),
          False,
        ),
      ],
    ),
  'Report a bug':                 embed(
    "Reporting a bug",
    "In order to report a bug add me on discord <@507642999992352779> and DM me the issue on hand and i will try to fix it. You may also suggest something to add/modify about the bot but I can't guarantee I will have the time to implement/modify that feature",
    color='#00ccff',
  ),
  'Credits':                      embed(
    "Credits",
"""
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>

RoboTop was really such a great bot. Perhaps the greatest i've ever used. After it shut down I really missed the reminders so I remade them! This is not my original idea, most of the looks and functionality is remade to be exactly (or really close to) original **[Colon](https://gdcolon.com)**'s bot and I just made it reminders-only.
"""[1:-1],
    color='#ff8000',
  ),
}
HELPMSG_NONE = embed(
  "General Help",
  'Use </help:1146216876779774012> with section specified to get more info about it.',
  fields=[
    (
      "Basic use",
"""
You don't need to use the robotop's prefix (`r!`) or any other prefix
The bot is mainly usable in DMs where `r!remind ` prefix is implied
Bot's credits and other statistics are available by using </botstatus:1146135130415579207>
View </help:1146216876779774012> with section argument set to `remind` for usage
"""[1:-1],
      False,
    ),(
      "Sections",
      ', '.join('`' + x + '`' for x in HELPMSGS),
      False,
    ),
  ],
  color='#00ccff',
)

def multichar_lstrip(input_string, text_to_remove):
    # Check if the input_string starts with the text_to_remove
    if input_string.startswith(text_to_remove):
        # If it does, remove the text_to_remove from the beginning of input_string
        return input_string[len(text_to_remove):]
    # If input_string doesn't start with text_to_remove, return it unchanged
    return input_string

class Reminder:
  unix = None
  text = None
  user = None
  def __init__(self, unix, text, user) -> None:
    self.unix = unix
    self.text = text
    self.user = user

  def __str__(self) -> str:
    return f'**{self.text}** (<t:{self.unix}:R>)'

### miru views

def VClearConfirm(func: t.Callable, _disabled=False, timeout=120) -> miru.View:
  class VClearConfirm_(miru.View):
    @miru.button(label='Confirm', style=hikari.ButtonStyle.DANGER, disabled=_disabled)
    async def btn_confirm(self, btn: miru.Button, ctx: miru.Context):
      await func(btn, ctx)

    if not _disabled:
      async def on_timeout(self) -> None:
        await self.message.edit(embed=EMBEDS.wipe(footer='❌ Did not cancel any reminders.'), components=VClearConfirm(func=func, _disabled=True).build())
        self.stop()
  return VClearConfirm_(timeout=timeout)

### sync funcs

def wipe_reminders(user_id) -> None:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / "reminders"
  with shelve.open(shelf_path, writeback=True) as shelf:
    if user_id in shelf: del shelf[user_id]

def get_ALL_reminders() -> dict[str, list[Reminder]]:
  shelf_path = SHELF_DIRECTORY / "reminders"
  with shelve.open(shelf_path, writeback=True) as shelf:
    return dict(shelf).copy()

def _get_reminders(key) -> list[Reminder]:
  shelf_path = SHELF_DIRECTORY / "reminders"
  with shelve.open(shelf_path, writeback=True) as shelf:
    return shelf.get(key, [])

def append_reminder(user_id, reminder: Reminder) -> Reminder:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / "reminders"
  with shelve.open(shelf_path, writeback=True) as shelf:
    if user_id in shelf:
      existing_values = shelf[user_id]
      existing_values.extend([reminder])
      shelf[user_id] = existing_values
    else:
      shelf[user_id] = [reminder]

def schedule_reminder(user_id, *, text, unix: int | str) -> bool:
  if isinstance(unix, str): unix = math.floor(time.time()+timestr_to_seconds(unix))
  if len(get_reminders(user_id)) < S.LIMITS.REMINDER:
    append_reminder(user_id, Reminder(unix=unix, text=text, user=user_id))
    return True
  return False

def get_reminders(user_id) -> list[Reminder]:
  user_id = str(user_id)
  return _get_reminders(user_id) or []

def delete_reminder_by_idx(user_id, idx: int) -> Reminder:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / "reminders"
  with shelve.open(shelf_path, writeback=True) as shelf:
    reminders = shelf.get(user_id) or []
    a = reminders[idx]
    del reminders[idx]
    shelf[user_id] = reminders
  return a

def is_valid_reminder_syntax(input_string):
  return bool(regex.match(SYNTAX_REGEX, input_string))

def timestr_to_seconds(timestr: str, *, unit='s'):
  timestr = timestr.replace(' ', '')
  if not timestr: return 0
  def is_numeric_or_dot(s: str) -> bool:
    return s.isnumeric() or s == '.'
  if not is_numeric_or_dot(timestr[0]): raise ValueError('non-empty timestr should start with a number or \'.\'')  # noqa: EM101

  timestr_lookup = {
    's':       1,
    'sec':     1,
    'secs':    1,
    'sex':     1,
    'second':  1,
    'seconds': 1,

    'm':       60,
    'min':     60,
    'mins':    60,
    'minute':  60,
    'minutes': 60,

    'h':     60*60,
    'hr':    60*60,
    'hrs':   60*60,
    'hour':  60*60,
    'hours': 60*60,

    'd':    24*60*60,
    'day':  24*60*60,
    'days': 24*60*60,

    'w':     7*24*60*60,
    'week':  7*24*60*60,
    'weeks': 7*24*60*60,

    'y':     356*24*60*60,
    'year':  356*24*60*60,
    'years': 356*24*60*60,

    'rev':         133*24*60*60, # 1 revolution = 133 days, nice if you get the reference hihi :>
    'revs':        133*24*60*60,
    'revolution':  133*24*60*60,
    'revolutions': 133*24*60*60,
  }

  def split_by_timestr(text: str):
    idxs = []
    for i in range(len(text)):
      if i == 0: continue
      if not is_numeric_or_dot(text[i-1]) and is_numeric_or_dot(text[i]):
        idxs.append(i)

    def split_string_at_idxs(input_string: str, idxs: list[int]):
      result = []
      start = 0

      for index in idxs:
        result.append(input_string[start:index])
        start = index

      # Append the remaining part of the string after the last split index
      result.append(input_string[start:])

      return result
    a = split_string_at_idxs(text, idxs)

    def split_level2(x: str):
      for i in range(len(x)):
        if i == 0: continue
        if is_numeric_or_dot(x[i-1]) and not is_numeric_or_dot(x[i]):
          splitidx = i
      return split_string_at_idxs(x, [splitidx])

    a = [split_level2(x) for x in a]

    try:
      a = [(float(value), unit) for (value, unit) in a]
    except ValueError as e:
      msg = f'Invalid timestr (float conversion): {timestr}'
      raise ValueError(msg) from e

    try:
      a = [timestr_lookup[unit]*value for (value, unit) in a]
    except KeyError as e:
      msg = f'Invalid timestr (invalid lookup): {timestr}'
      raise ValueError(msg) from e

    return sum(a)

  try:
    unit_divisor = timestr_lookup[unit]
  except KeyError as e:
    msg = f'Invalid output unit: {unit}'
    raise ValueError(msg) from e
  else:
    return (split_by_timestr(timestr) / unit_divisor)

def author_dict(author, url=None, *, discriminator=False, footer=False):
  if author is None: # or S.HIDE_AUTHORS
    return None
  if not url or footer:
    return {('text' if footer else 'name'): f'{author.username!s}#{author.discriminator!s}' if discriminator else str(author.username), 'icon': author.avatar_url}
  if isinstance(url, bool):
    return {
      'name':
      f'{author.username!s}#{author.discriminator!s}'
      if discriminator else str(author.username),
      'icon':
      author.avatar_url,
      'url':
      author.avatar_url,
    }
  return {
    'name':
    f'{author.username!s}#{author.discriminator!s}'
    if discriminator else str(author.username),
    'icon':
    author.avatar_url,
    'url':
    url,
  }

def uptime():
  delta = datetime.datetime.now(tz=tz.get_localzone()) - start_time
  total_seconds = delta.total_seconds()
  days = total_seconds // 86400
  hours = (total_seconds // 3600) % 24
  minutes = (total_seconds // 60) % 60
  seconds = total_seconds % 60
  if days > 0:
    return f"{int(days)}d + {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
  return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def seconds_to_timestr(seconds: int) -> str:
  units = [
    ("day", 86400),
    ("hour", 3600),
    ("minute", 60),
    ("second",  1),
  ]

  for unit, value_in_seconds in units:
    if seconds >= value_in_seconds:
        num_units = seconds / value_in_seconds
        if num_units == round(num_units): num_units = round(num_units)
        num_units = round(num_units, 2)
        unit_str = unit if num_units == 1 else unit + 's'
        return f"{num_units} {unit_str}"

  # If seconds is 0, return "in 0 seconds"
  return "0 seconds"

def random_sure() -> str:
  return rng.choice(list({
    'Roger!',
    'Sure thing!',
    'Got it!',
    'Epic!',
    'Heck yeah!',
    'Awesome!',
    'Noted!',
    'Sounds good!',
    'All done!',
    'Great!',
    'Gotcha!',
  }))

### async funcs

async def get_guild_count(bot: lb.BotApp):
  return len(await bot.rest.fetch_my_guilds())









