if True:  # \/ Imports
  import sys

  if sys.version_info[:2] != (3, 11):
    raise NotImplementedError('Use python 3.11')
  import asyncio
  import contextlib
  import datetime
  import math
  import os
  import pathlib as p
  import random as rng
  import re as regex
  import shelve
  import string
  import subprocess
  import time
  import typing as t
  from collections.abc import Callable, Iterable, Mapping, Sequence
  from typing import Any

  import hikari
  import lightbulb as lb
  import pytz
  import tcrutils as tcr
  from lightbulb.ext import tasks
  from tcrutils import *
  from tcrutils import error as TCRError

  import miru_v3 as miru
  import settings as S


class Tz:
  def get_localzone(self):
    return pytz.timezone('Europe/Warsaw')


tz = Tz()

if True:  # \/ Critical Funcs do not touch

  def F(item: str) -> str:
    return eval(f'f{item!r}')

  def embed(
    title: str,
    description: str,
    *,
    url=None,
    color=None,
    timestamp=None,
    thumbnail=None,
    footer=None,
    footer_icon=None,
    author: dict | None = None,
    image=None,
    fields: list | None = None,
  ) -> hikari.Embed:
    if (title is not Null and not title.strip()) or (
      description is not Null and not description.strip()
    ):
      msg = f'Both title and description must be non-whitespace-only strings unless explicitly specified the title to be Null, got Title: {title!r}, Description: {description!r}'
      raise ValueError(msg)

    if fields is None:
      fields = []

    if author is None:
      author = {}

    out = hikari.Embed(
      title=title if title is not Null else None,
      description=description if description is not Null else None,
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

  start_time = datetime.datetime.now(tz=tz.get_localzone())

TOKEN2_FILE = p.Path('TOKEN2.txt')
TOKEN_FILE = p.Path('TOKEN.txt')
USING_TOKEN2 = False
if os.name == 'nt' and TOKEN2_FILE.is_file() and S.USE_TEST_TOKEN_IF_AVAILABLE:
  TOKEN_FILE = TOKEN2_FILE
  USING_TOKEN2 = True
try:
  ('..' / TOKEN_FILE).is_file()
except PermissionError:
  pass
else:
  if not TOKEN_FILE.is_file():
    TOKEN_FILE = '..' / TOKEN_FILE
try:
  ('..' / TOKEN_FILE).is_file()
except PermissionError:
  pass
else:
  if not TOKEN_FILE.is_file():
    TOKEN_FILE = '..' / TOKEN_FILE
if not TOKEN_FILE.is_file():
  console.critical('Unable to find TOKEN.txt file')
  sys.exit(1)
if not TOKEN_FILE.read_text(encoding='UTF-8'):
  console.critical('The TOKEN.txt file is empty.')
  sys.exit(1)
TOKEN = TOKEN_FILE.read_text(encoding='UTF-8')
TOKEN = TOKEN.strip()

if USING_TOKEN2:
  S.MAIN_COLOR = (
    S.MAIN_COLOR_ALT
  )  # If the bot is in test mode use the alternative main color for embeds

NEWLINE = '\n'
APOSTROPHE = "'"
FAKE_PIPE = '¦'
BACKSLASH = '\\'
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # noqa: PTH120, PTH100
try:
  SHELF_DIRECTORY = p.Path('./db') if os.name == 'nt' else p.Path('./../../RoboBottomDB')
  SHELF_DIRECTORY.mkdir(
    exist_ok=True, parents=True
  )  # When hosting on termux on my phone make the reminders global for all versions that have this line (v1.0.3 and higher)
except PermissionError:
  SHELF_DIRECTORY = p.Path('../RoboBottomDB')
  SHELF_DIRECTORY.mkdir(exist_ok=True, parents=True)

# REGEX_ONLY_DELAY: str = timestr.pattern.replace('^', '').replace('$', '') #r'^(?:(?:(?:[1-9]\d*\.\d+)|(?:\.?\d+))[a-zA-Z]+)+'
# SYNTAX_REGEX: str     = REGEX_ONLY_DELAY + r" +(?:.|\s)+$" #r'^(?:(?:(?:[1-9]\d*\.\d+)|(?:\.?\d+))[a-zA-Z]+)+ +(?:.|\s)+$'


class ReminderFlag:
  NONE = 0
  IMPORTANT = 1 << 0
  RECURRING = 1 << 1
  HIDDEN = 1 << 2


class ReminderFlagSymbol:
  __SYMBOLS__ = None
  IMPORTANT = '!'
  RECURRING = '&'
  HIDDEN = '#'


assert {x for x in ReminderFlag.__dict__ if x != 'NONE' and '_' not in x} == {
  x for x in ReminderFlagSymbol.__dict__ if x != 'NONE' and '_' not in x
}, 'Non-corresponding flags in ReminderFlag and ReminderFlagSymbol classes'

ReminderFlagSymbol.__SYMBOLS__ = tuple(
  {x: y for x, y in ReminderFlagSymbol.__dict__.items() if '_' not in x}.values()
)


class Reminder:
  unix = None  # The time of the reminder (int | str)
  text = None  # The text of the reminder (str)
  user = None  # Discord User ID (int | str)
  flag = 0  # Any reminders created before addition of the flags will have flags=0 after the reboot to the new version

  def __init__(self, unix, text, user, flag: int | None) -> None:
    self.unix = unix
    self.text = text
    self.user = user
    self.flag = flag

  def __str__(self) -> str:
    return f'**{self.text}** (<t:{self.unix}:R>)'

  def __repr__(self) -> str:
    hidden = self.flag & ReminderFlag.HIDDEN
    return f'{flags_to_str(self.flag)}/{"#" if hidden else ""}{self.text if not hidden else random_str_of_len(max(1, len(self.text)-2))}{"#" if hidden else ""}/'


class Embeds:
  def e_generic_error(self, e: Exception, *, author=None, **kwargs):
    # return embed(*extract_error(e, raw=True), color=0xFF0000, author=author_dict(author), **kwargs)
    return embed(
      *extract_error(e, raw=True),
      color=('#FF8000' if rng.randint(1, 100) == 1 else '#FF0000'),
      footer=(S.OOPSIE_WOOPSIE if rng.randint(1, 100) == 1 else ''),
      **kwargs,
    )  # Oopsie Woopsie :3

  def invalid_syntax_small(self, e: Exception | None = None):
    return embed(
      'Invalid syntax',
      'To view syntax guide use the </help:1146446941278965793> with section set to `Remind - Syntax`',
      color='#ff0000' if rng.randint(1, 100) != 1 else '#ff8000',
      footer=None if e is None else extract_error(e),
    )

  def invalid_syntax_big(self, _in_help=False):
    return embed(
      'Invalid syntax' if not _in_help else 'Reminders',
      'Provide a delay in the format of at least one `[NUMBER][UNIT]` group or multiple for example `30m` or `1y30w` or `1h.25d` then separate it with a space and provide your message. The message must be between 1 and 100 characters long and must be separated from the delay with a space.\nAdditionally make sure all units are correct',
      fields=[
        (
          'Examples',
          '`5h59m rescue                 `\n`1h BUY THE GD COLOGNE PLUSHIE`\n`3h.5d praise senko           `',
          True,
        ),
        (
          'Uh.. also example',
          """
`10h50m finish this discord bot`
`^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^`
` time        your message     `
"""[1:-1],
          True,
        ),
        (
          'Units',
          '`s`, `sec`, `seconds`\n`m`, `min`, `minutes`\n`h`, `hr`, `hours`\n`w`, `weeks`\n`y`, `years`\n`pul`, `pull`, `card` alias for `11.5h`\n`res`, `rescues` alias for `6h`\n`???`, `???????????` (easteregg/hidden reference)\nAll singular/plural versions of the nouns should be valid as well',
          False,
        ),
        (
          'Special aliases',
          '`pul` -> `1pul pul`\n`card` -> `1card card`\n`rescue` -> `1rescue rescue`\n`<anything not containing space>` -> `<said thing> <said thing>`\nFor example `1h` -> `1h 1h`',
          False,
        ),
        (
          'Prefixes / Modifiers / Flags',
          "`!` - **Important**: Will ping you when reminded\n`#` - **Hidden**: Will hide the reminder's contents until you're reminded\n`&` - **Recurring** - Will re-schedule the reminder after sending it\n\n**How to use it?** Just prepend anything you type in with one or multiple flags in any order for example:\n`!6m pet the Colon plushie`\n`!&1d find another xss vulnerability in zoo bot`\n`#999y No one will ever see this reminder's contents`\n\nIf certain reminder has any flags, their symbols will be shown next to them in reminders list",
          False,
        ),
      ],
      footer=f'Regex for validating the reminder text:\n/{timestr.pattern}/gi'[:2000],
      color='#ff0000' if not _in_help else S.MAIN_COLOR,
    )

  def invalid_syntax_cancel(self, n=99999, do_what='cancel'):
    return embed(
      'Invalid syntax/choice',
      f'Use the following syntax: `{do_what} <1-{n}>`'
      if n > 0
      else f"You don't have any reminders to {do_what}, therefore every number you choose will result in invalid choice",
      color='#ff0000',
    )

  def cancel_success(self, reminder: Reminder):
    return embed(
      '🔕 Reminder cancelled!',
      reminder.text[:3950]
      if not reminder.flag & ReminderFlag.HIDDEN
      else 'Its contents have been unrecoverably lost!',  # + f'\n||(It would trigger <t:{reminder.unix}:R> if you didn\'t cancel)||',
      color=('#ff0000' if rng.randint(1, 100) != '1' else '#ff8000'),
    )

  def reminder(self, reminder: Reminder, rem_id: int):
    hidden = reminder.flag & ReminderFlag.HIDDEN
    return embed(
      f"📝 {'Hidden ' if hidden else ''}Reminder #{rem_id+1}",
      reminder.text
      if not hidden
      else "`>> This reminder is hidden! <<`\nIts contents will only be shown when it's triggered, not cancelled",
      color=S.MAIN_COLOR,
      footer=f'Will trigger in {timestr.to_str(reminder.unix - math.floor(time.time()))} ({timestr.to_datestr_from_unix(reminder.unix)})',
    )

  def wipe(self, footer=None):
    return embed(
      'Are you sure?',
      'This will cancel **ALL** your reminders!',
      color=('#ff0000' if rng.randint(1, 100) != '1' else '#ff8000'),
      footer=footer,
    )

  def list_(
    self,
    rems: Sequence[Reminder],
    *,
    who: str | None = None,
    total_override: Any | None = None,
    count_from: int = 0,
  ) -> hikari.Embed:
    patt = '`%s`'
    display_rems = '\n'.join(
      [
        f'{i+1+count_from}) {((patt % flags_to_str(x.flag) + " ") if x.flag else "")}**{cut_at(x.text, S.LIST_MAX_CHAR_COUNT_PER_REMINDER, filter_links=f"[{BACKSLASH}3...]", shrink_links_visually_if_fits=True).replace(NEWLINE, " ").rstrip(BACKSLASH).replace("**", f"{BACKSLASH}*{BACKSLASH}*").replace(BACKTICKS, 3*APOSTROPHE) if not x.flag & ReminderFlag.HIDDEN else f"`{random_str_of_len(min(50, rng.randint(max(1, len(x.text[:S.LIST_MAX_CHAR_COUNT_PER_REMINDER])-2), len(x.text[:S.LIST_MAX_CHAR_COUNT_PER_REMINDER])+2)))}`"}** (<t:{x.unix}:R>)'
        for i, x in enumerate(rems)
      ],
    )
    if display_rems:
      display_rems += '\n\n'
    rest = f'Cancel a reminder with `cancel [1-{len(rems) if total_override is None else total_override}]`'
    return embed(
      f"{'Your' if who is None else ((who + APOSTROPHE + 's') if not who.endswith('s') else (who + APOSTROPHE))} reminders ({len(rems) if total_override is None else total_override})",
      f'{display_rems}{rest}'.rstrip('\n'),
      color=S.MAIN_COLOR,
    )

  def no_reply(self):
    return embed(
      'Unsupported reply action',
      'This message does not support reply action',
      color='ff0000',
    )


EMBEDS = Embeds()




def multichar_lstrip(input_string, text_to_remove):
  if input_string.startswith(text_to_remove):
    return input_string[len(text_to_remove) :]
  return input_string


### miru views


def VClearConfirm(func: t.Callable, _disabled=False, timeout=120) -> miru.View:
  class VClearConfirm_(miru.View):
    @miru.button(label='Confirm', style=hikari.ButtonStyle.DANGER, disabled=_disabled)
    async def btn_confirm(self, btn: miru.Button, ctx: miru.Context):
      await func(btn, ctx)

    if not _disabled:

      async def on_timeout(self) -> None:
        await self.message.edit(
          embed=EMBEDS.wipe(footer='❌ Did not cancel any reminders.'),
          components=VClearConfirm(func=func, _disabled=True).build(),
        )
        self.stop()

  return VClearConfirm_(timeout=timeout)


def VReminder(
  reminder: Reminder, rem_id: int, *, _activated=False, _disabled=False, timeout=120
) -> miru.View:
  class VReminder_(miru.View):
    if not _activated:

      @miru.button(label='...', style=hikari.ButtonStyle.SECONDARY, disabled=_disabled)
      async def btn_more_options(self, btn: miru.Button, ctx: miru.Context):
        view = VReminder(reminder=reminder, rem_id=rem_id, _activated=True)
        await self.message.edit(EMBEDS.reminder(reminder, rem_id), components=view.build())
        await view.start(self.message)
    else:

      async def reschedule(self, time):
        delete_reminder_by_idx()
        await schedule_reminder()

      @miru.button(emoji='✏', style=hikari.ButtonStyle.PRIMARY, disabled=_disabled, row=1)
      async def btn_p3(self, btn: miru.Button, ctx: miru.Context):
        await self.reschedule()

      @miru.button(label='+10m', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=1)
      async def btn_p1(self, btn: miru.Button, ctx: miru.Context):
        await self.reschedule('10m')

      @miru.button(label='+1h', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=1)
      async def btn_p2(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(label='+6h', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=1)
      async def btn_p4(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(label='+1d', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=1)
      async def btn_p5(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(emoji='❌', style=hikari.ButtonStyle.DANGER, disabled=_disabled, row=2)
      async def btn_m3(self, btn: miru.Button, ctx: miru.Context):
        return delete_reminder_by_idx(reminder.user, rem_id)

      @miru.button(label='-10m', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=2)
      async def btn_m1(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(label='-1h', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=2)
      async def btn_m2(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(label='-6h', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=2)
      async def btn_m4(self, btn: miru.Button, ctx: miru.Context):
        return 0

      @miru.button(label='-1d', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled, row=2)
      async def btn_m5(self, btn: miru.Button, ctx: miru.Context):
        return 0

    if not _disabled:

      async def on_timeout(self) -> None:
        await self.message.edit(EMBEDS.reminder(reminder, rem_id), components=[])
        self.stop()

  return VReminder_(timeout=timeout, autodefer=True)


def VPagedMessage(
  pages: Sequence[Mapping],
  page: int,
  _disabled=False,
  timeout: float | None = 120,
) -> miru.View:
  if len(pages) == 0:
    msg = 'pages iterable is empty'
    raise ValueError(msg)

  if not (0 <= page < len(pages)):
    msg = f'invalid page number: {page}'
    raise ValueError(msg)

  class VPagedMessage_(miru.View):
    @miru.button(
      label=f'<< Page {page}', style=hikari.ButtonStyle.SUCCESS, disabled=_disabled or (page == 0)
    )
    async def btn_prev(self, btn: miru.Button, ctx: miru.Context):
      view = VPagedMessage(pages=pages, page=page - 1)
      self.stop()
      # await ctx.respond()
      await ctx.edit_response(**(pages[page - 1]), components=view.build())
      await view.start(self.message)
      await view.wait()

    @miru.button(
      label=f'Page {page+2} >>',
      style=hikari.ButtonStyle.SUCCESS,
      disabled=_disabled or (page == len(pages) - 1),
    )
    async def btn_next(self, btn: miru.Button, ctx: miru.Context):
      view = VPagedMessage(pages=pages, page=page + 1)
      self.stop()
      # await ctx.respond()
      await ctx.edit_response(**(pages[page + 1]), components=view.build())
      await view.start(self.message)
      await view.wait()

    if not _disabled:

      async def on_timeout(self) -> None:
        await self.message.edit(
          components=VPagedMessage(pages=pages, page=page, _disabled=True).build()
        )
        self.stop()

  return VPagedMessage_(timeout=timeout)


### sync funcs


def wipe_reminders(user_id) -> None:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    if user_id in shelf:
      del shelf[user_id]


def get_ALL_reminders() -> dict[str, list[Reminder]]:
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    return dict(shelf).copy()


ALL = get_ALL_reminders


def _get_reminders(key) -> list[Reminder]:
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    return shelf.get(key, [])


def _sort_reminders(user_id) -> None:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / 'reminders'
  rems = get_reminders(user_id)

  def key(rem: Reminder):
    return rem.unix

  rems = sorted(rems, key=key, reverse=True)
  with shelve.open(shelf_path, writeback=True) as shelf:
    shelf[user_id] = rems


def append_reminder(user_id, reminder: Reminder) -> Reminder:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    if user_id in shelf:
      existing_values = shelf[user_id]
      existing_values.extend([reminder])
      shelf[user_id] = existing_values
    else:
      shelf[user_id] = [reminder]
  _sort_reminders(user_id)


def schedule_reminder(user_id, *, text, unix: int | str, flags=ReminderFlag.NONE) -> bool:
  if isinstance(unix, str):
    unix = math.floor(time.time() + timestr.to_int(unix))
  if len(get_reminders(user_id)) < S.LIMITS.REMINDER:
    append_reminder(user_id, Reminder(unix=unix, text=text, user=user_id, flag=flags))
    _sort_reminders(user_id)
    return True
  return False


def get_reminders(user_id) -> list[Reminder]:
  user_id = str(user_id)
  return _get_reminders(user_id) or []


def delete_reminder_by_idx(user_id, idx: int) -> Reminder:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    reminders = shelf.get(user_id) or []
    if len(reminders) - 1 < idx:
      return console.error(f'Tried to delete reminder #{idx+1} but only {len(reminders)}')
    a = reminders[idx]
    del reminders[idx]
    shelf[user_id] = reminders
  return a


def delete_reminder_by_reminder(user_id, reminder: Reminder) -> None:
  user_id = str(user_id)
  shelf_path = SHELF_DIRECTORY / 'reminders'
  with shelve.open(shelf_path, writeback=True) as shelf:
    reminders = shelf.get(user_id) or []
    reminders_old = reminders
    try:
      reminders = [rem for rem in reminders if rem.unix != reminder.unix]
      assert reminders_old != reminders
    except (ValueError, AssertionError):
      console.error(f"Unable to delete reminder {reminder!r} - It's not present")
    shelf[user_id] = reminders


def is_valid_reminder_syntax(input_string) -> bool:
  return timestr.valid(input_string.split(' ')[0])
  # return bool(regex.match(SYNTAX_REGEX, input_string))


def seconds_to_nearest_hour_minute(hour, minute):
  # Get the current time in seconds since the epoch
  current_time = int(time.time())

  # Calculate the current hour and minute
  current_struct_time = time.localtime(current_time)
  current_hour = current_struct_time.tm_hour
  current_minute = current_struct_time.tm_min

  # Calculate the number of seconds until the specified time
  return ((hour - current_hour) * 3600 + (minute - current_minute) * 60) % 86400


def author_dict(author, url=None, *, discriminator=False, footer=False):
  if author is None:  # or S.HIDE_AUTHORS
    return None
  if not url or footer:
    return {
      ('text' if footer else 'name'): f'{author.username!s}#{author.discriminator!s}'
      if discriminator
      else str(author.username),
      'icon': author.avatar_url,
    }
  if isinstance(url, bool):
    return {
      'name': f'{author.username!s}#{author.discriminator!s}'
      if discriminator
      else str(author.username),
      'icon': author.avatar_url,
      'url': author.avatar_url,
    }
  return {
    'name': f'{author.username!s}#{author.discriminator!s}'
    if discriminator
    else str(author.username),
    'icon': author.avatar_url,
    'url': url,
  }


def uptime():
  delta = datetime.datetime.now(tz=tz.get_localzone()) - start_time
  total_seconds = delta.total_seconds()
  days = total_seconds // 86400
  hours = (total_seconds // 3600) % 24
  minutes = (total_seconds // 60) % 60
  seconds = total_seconds % 60
  if days > 0:
    return f'{int(days)}d + {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
  return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'


def seconds_to_timestr(seconds: int) -> str:
  units = [
    ('day', 86400),
    ('hour', 3600),
    ('minute', 60),
    ('second', 1),
  ]

  for unit, value_in_seconds in units:
    if seconds >= value_in_seconds:
      num_units = seconds / value_in_seconds
      if num_units == round(num_units):
        num_units = round(num_units)
      num_units = round(num_units, 2)
      unit_str = unit if num_units == 1 else unit + 's'
      return f'{num_units} {unit_str}'

  # If seconds is 0, return "in 0 seconds"
  return '0 seconds'


def random_sure() -> str:
  return rng.choice(
    list(
      {
        'Done',
        'Got it',
        'Sweet',
        'Awesome',
        'Great',
        'Roger',
        'Epic',
        'Gotcha',
        'Noted',
        'Sure thing',
        'Sounds good',
        'Heck yeah',
        'All done',
      }
    )
  )


def get_stats(a: int = 0) -> tuple[int, int]:
  ALL_rems = get_ALL_reminders()
  if a == 0:
    return len(ALL_rems)
  return sum([len(x) for x in ALL_rems.values()])


def parse_for_aliases(content: str, is_reply: bool = False) -> str | None:
  if content is None:
    return None
  if content in ['1pul', 'pul']:
    return '1pul pul'
  if content in ['1card', 'card']:
    return '1card card'
  if content in ['1rescue', 'rescue']:
    return '1rescue rescue'
  if not ([x for x in content if x.isalpha()] and [x for x in content if x.isnumeric()]):
    return content
  if ' ' not in content and not is_reply:
    return f'{content} {content}'
  return content


def testmode() -> str:
  """Return suffix when called, may be used in if check since it returns a falsey '' when not in testmode and truey '...' if in testmode."""
  return ' - Testmode' if USING_TOKEN2 else ''


def separate_flags_from_rest(content: str) -> tuple[int, str]:
  i = 0
  for letter in content:
    if letter not in ReminderFlagSymbol.__SYMBOLS__:
      break
    i += 1
  flags, content = content[:i], content[i:]
  flags = ''.join(sorted(set(flags)))
  fls = 0
  for FLAG, VALUE in {
    x: y for x, y in ReminderFlag.__dict__.items() if '_' not in x and x != 'NONE'
  }.items():
    fls = fls | ((getattr(ReminderFlagSymbol, FLAG) in flags) * VALUE)
  return fls, content


def flags_to_str(flags: int):
  text = ''
  for FLAG, VALUE in {
    x: y for x, y in ReminderFlag.__dict__.items() if x != 'NONE' and '_' not in x
  }.items():
    if flags & VALUE:
      text += getattr(ReminderFlagSymbol, FLAG)
  return ''.join(sorted(text))


def random_str_of_len(n: int, pool: None | str = None, banned: None | Sequence[str] = None):
  if banned is None:
    banned = ['`', '*', '_']
  if pool is None:
    pool = (
      string.ascii_letters
      + string.digits
      + string.punctuation
      + string.punctuation
      + string.punctuation
      + string.punctuation
      + string.punctuation
    )
  out = ''
  for _ in range(n):
    out += rng.choice([x for x in pool if x not in banned])
  return out


def get_battery_dict() -> None | dict[str, t.Any]:
  """Return None if there's no battery."""
  if USING_TOKEN2:  # Fake battery if on test token
    return {
      'health': 'SHIT',
      'percentage': rng.randint(1, 99),
      'plugged': f"{'UN' if (discharging := rng.randint(1, 3) != 1) else ''}PLUGGED{'_AC' if not discharging else ''}",
      'status': f"{'DIS' if discharging else ''}CHARGING",
      'temperature': {rng.uniform(26, 33)},
      'current': rng.randint(527400 // 2, 527400 * 2) * (-2 if discharging else 1),
    }
  try:
    return eval(subprocess.check_output('termux-battery-status', shell=True).decode('utf-8'))
  except Exception as e:
    console.error(extract_error(e))
    return None


class Battery:
  health: str
  percentage: int
  plugged: str
  status: str
  temperature: float
  current: int

  def __init__(self, *, health, percentage, plugged, status, temperature, current) -> None:
    self.health = health
    self.percentage = percentage
    self.plugged = plugged
    self.status = status
    self.temperature = temperature
    self.current = current

  update = __init__

  def __str__(self) -> str:
    charging = self.status in ['CHARGING', 'FULL']
    if not charging and self.percentage < 25:
      icon = '🔋 ❗❗'
    elif charging:
      icon = '🔌'
    else:
      icon = '🔋'
    return (
      f"{self.percentage if self.percentage != 69 else '69.420'}%{(' ' + icon) if icon else ''}"
    )


_battery: None | Battery = None


def get_battery() -> Null | 'Battery':
  global _battery
  a = get_battery_dict()
  if a is not None:
    if _battery is None:
      _battery = Battery(**a)
    else:
      _battery.update(**a)
    return _battery
  return Null


### async funcs


async def get_guild_count(bot: lb.BotApp):
  return len(await bot.rest.fetch_my_guilds())


async def trigger_and_delete_reminder(user_id: int | str, reminder: Reminder, remindfunc):
  user_id = str(user_id)
  delete_reminder_by_reminder(user_id, reminder)
  difference = abs(reminder.unix - time.time())
  if difference < S.TOO_LATE_THRESHOLD_SECONDS:
    difference = 0
  await remindfunc(
    user_id,
    reminder.text,
    difference,
    ping_user=bool(reminder.flag & ReminderFlag.IMPORTANT),
    hide_text=bool(reminder.flag & ReminderFlag.HIDDEN),
  )


async def update_activity(
  bot: lb.BotApp, text: str = S.DEFAULT_ACTIVITY_TEXT, *, activity_type=hikari.ActivityType.CUSTOM
) -> None:
  await bot.update_presence(activity=hikari.Activity(name=str(text), type=activity_type))


async def send_paged_message_and_wait(
  responder, pages: Sequence[Mapping], page: int = 0, timeout: float | None = 120
) -> dict:
  if page < 0:
    page = page % len(pages)
  view = VPagedMessage(pages=pages, page=page, timeout=timeout)
  message = await responder(**pages[page], components=view.build())
  await view.start(message)
  await view.wait()


HELPMSG_NONE = embed(
  'General Help',
  'Use </help:1146216876779774012> with section specified to get more info about it.',
  fields=[
    (
      'Basic use',
      """
You don't need to use the robotop's prefix (`r!`) or any other prefix
The bot is mainly usable in DMs where `r!remind ` prefix is implied
It can also be used on servers with `/cmds` but all messages are ephemeral
Bot's status and other statistics are available by using </botstatus:1146135130415579207>
View credits by using </help:1146216876779774012> with section set to `Credits`
View </help:1146216876779774012> with section argument set to `remind` for usage
"""[1:-1],
      False,
    ),
  ],
  color=S.MAIN_COLOR,
)
HELPMSGS = {
  'Introduction': HELPMSG_NONE,
  'Remind - Syntax': EMBEDS.invalid_syntax_big(_in_help=True),
  'List your reminders': embed(
    'List of reminders',
    'Simple. Shows you the list of reminders.',
    color=S.MAIN_COLOR,
    fields=[
      (
        'Usage & Example',
        '`list`',
        False,
      ),
      (
        'Aliases',
        ', '.join(['`' + x + '`' for x in S.ALIASES.LIST]),
        False,
      ),
    ],
  ),
  'Cancel a reminder': embed(
    'Cancelling Reminders',
    'Use the following syntax: `cancel <1-99999>` where you specify the index of the reminder that you want to cancel.\nTo see the list of your reminders along with the indices type `list` or view its help by using </help:1146216876779774012> with section argument `list`',
    color=S.MAIN_COLOR,
    fields=[
      (
        'Example',
        '`cancel 1`',
        False,
      ),
    ],
  ),
  'Clear (cancel) all reminders': embed(
    'Clearing all reminders',
    'To clear (cancel) all reminders type `clear` (or any of its aliases) and it will remove all of your set reminders without reminding you',
    color=S.MAIN_COLOR,
    fields=[
      (
        'Aliases',
        ', '.join(['`' + x + '`' for x in S.ALIASES.WIPE]),
        False,
      ),
    ],
  ),
  'Delete bot messages': embed(
    "Deleting bot's messages",
    'There are two ways...',
    fields=[
      (
        'In bulk',
        'Use the </delhistory:1153087533954113726> slash command in DMs to delete all messages in that channel that were sent by the bot. You will still have to delete your messages yourself. **__Be careful with this one!__**',
        False,
      ),
      (
        'One at a time',
        f"Reply to a message you want to delete and as the message text send any of the following:\n{', '.join(f'`{x}`' for x in S.ALIASES.DELETE)}",
        False,
      ),
    ],
    color=S.MAIN_COLOR,
  ),
  'Reply Actions': embed(
    'Reply actions',
    'To use reply actions reply to a message containing a reminder (Embed title must have `reminder`) and in your message provide only the time part of the reminder, for example: `1h20m`. This will intepret it as inhereting the reminder text from the replied-to message.',
    color=S.MAIN_COLOR,
    fields=[
      (
        'Flags',
        'Flags are not supported, for now at least - if you use this method all message flags are zeroed out and if the message starts and ends with spoiler tags (hidden reminder) they are removed.',
        False,
      ),
    ],
  ),
  'Report a bug': embed(
    'Reporting a bug',
    "In order to report a bug add me on discord <@507642999992352779> and DM me the issue on hand and i will try to fix it. You may also suggest something to add/modify about the bot but I can't guarantee I will have the time to implement/modify that feature",
    color=S.MAIN_COLOR,
  ),
  'Credits': embed(
    'Credits',
    """
**Originally created by:** **[Colon](https://gdcolon.com)** <:fluff:1146072273665654864>
**Recreated by:** <@507642999992352779>

RoboTop was really such a great bot. Perhaps the greatest i've ever used. After it shut down I really missed the reminders so I remade them! This is __not__ my original idea, most of the looks and functionality is remade to be exactly (or really close to) original **[Colon](https://gdcolon.com)**'s bot and I just made it reminders-only.
"""[1:-1],
    color='#ff8000',
  ),
  'How to host this bot yourself': embed(
    'How to host this bot',
    "Detailed instruction is available **[here](https://github.com/TheCreatorrr333/RoboBottom)** as well as the bot's source code",
    color=S.MAIN_COLOR,
  ),
}