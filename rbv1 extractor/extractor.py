import json
import pathlib as p
import shelve
from typing import TypedDict as TD

import tcrutils as tcr
from tcrutils import c

INDENT = 2

imports_path = p.Path('./imports.py')

if not imports_path.exists():
  IMPORTS = """
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
    return f'/{self.text}/'
"""[1:-1]

  with imports_path.open('w') as f:
    f.write(IMPORTS)

class ReminderFlag:
  NONE = 0
  IMPORTANT = 1 << 0
  RECURRING = 1 << 1
  HIDDEN = 1 << 2

class CTF:
  NONE = 0
  """No special flags are set."""
  HASH_HIDDEN = 1 << 0
  """The reminder contents are hidden from the user until the reminder is triggered."""
  IMPORTANT = 1 << 1
  """Upon invokation the reminder is delivered with a user @mention."""

try:
  path = p.Path(tcr.insist(
    lambda: input("Enter path to db [./reminders]: "),
    lambda x: (not x and p.Path('./reminders').is_file()) or p.Path(x).is_file(),
    lambda: input("Enter path to db (file must exist): ")
  ) or "./reminders")
except KeyboardInterrupt:
  print()
  exit()

db = shelve.open(path)
valid_keys = [int(x) if tcr.able(int, x) else x for x in db]
c(valid_keys)

try:
  user_id = int(tcr.insist(
    lambda: input("Enter user ID [ALL IDS]: "),
    lambda x: not x or (tcr.able(int, x) and int(x) in valid_keys),
    lambda: input("Enter user ID (must be in the above list): ")
  ) or -1)
except KeyboardInterrupt:
  print()
  exit()

class ExportedDataReminderTD(TD):
  unix: int
  text: str
  tstr: str
  offset: int
  flags: int
  created_at: int
  priority: int
  recursion_tstr: str
  attachment_urls: list[str]

class ExportedDataTD(TD):
  reminders: list[ExportedDataReminderTD]

def convert_old_to_new_flag(x: int) -> int:
  HIDDEN, IMPORTANT = x & ReminderFlag.HIDDEN, x & ReminderFlag.IMPORTANT

  flags = CTF.NONE

  if HIDDEN:
    flags |= CTF.HASH_HIDDEN

  if IMPORTANT:
    flags |= CTF.IMPORTANT

  return flags

def extract_reminders(user_id: int) -> ExportedDataTD:
  r = db[str(user_id)]

  return {
    "reminders": [
      {
        "unix": x.unix,
        "text": x.text,
        "tstr": '-1s',
        "offset": 0,
        "flags": convert_old_to_new_flag(x.flag),
        "created_at": 0,
        "priority": 0,
        "recursion_tstr": "",
        "attachment_urls": []
      }
      for x in r
    ]
  }

outdir = (path.parent / 'out')

if outdir.exists() and not outdir.is_dir():
  raise FileExistsError('out directory already exists and is not a directory')

outdir.mkdir(exist_ok=True)

if user_id == -1:
  for key in valid_keys:
    extracted = extract_reminders(key)

    filename = path.name + f'-{key}.json'

    with (outdir / filename).open('w') as f:
      json.dump(extracted, f, indent=INDENT)
else:
  extracted = extract_reminders(user_id)

  filename = path.name + f'{user_id}.json'

  with (outdir / filename).open('w') as f:
    json.dump(extracted, f, indent=INDENT)
