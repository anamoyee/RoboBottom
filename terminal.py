from typing import Literal, TypedDict

from imports import *

TERMINAL_SHELF_DIRECTORY = SHELF_DIRECTORY / 'user_db'
TERMINAL_SHELF_DIRECTORY.mkdir(exist_ok=True)


class FSObject(TypedDict):
  type: 'File | Directory'
  name: str
  hidden: bool


class Directory(FSObject):
  directory: Iterable[FSObject]


class File(FSObject):
  type: 'File | TextFile | ImageFile'


class TextFile(File):
  type: 'TextFile'
  text: str


class ImageFile(File):
  type: 'ImageFile'
  image_strpath: str


FSObject._DEFAULT = {
  'type': File,
  'name': 'eph ess object',
  'hidden': False,
}

Directory._DEFAULT = {
  **FSObject._DEFAULT,
  'type': Directory,
  'directory': (),
}

File._DEFAULT = {
  **FSObject._DEFAULT,
  'type': File,
}

TextFile._DEFAULT = {
  **File._DEFAULT,
  'text': '',
}

ImageFile._DEFAULT = {
  **File._DEFAULT,
  'image_strpath': '',
}

file_ts = [y for x, y in globals().items() if x.endswith('File')]

emoji_lookup = {
  None: '❔',
  Directory: '📁',
  ImageFile: '🌄',
  TextFile: '🗒️',
}


class UserDB:
  s: shelve.Shelf
  user_id: int

  @staticmethod
  def _get_user_shelf_path(user_id: int | str):
    (TERMINAL_SHELF_DIRECTORY / str(user_id)).mkdir(exist_ok=True)
    return TERMINAL_SHELF_DIRECTORY / str(user_id) / str(user_id)

  def __init__(self, user_id: str | int):
    self.user_id = int(user_id)
    self.s = shelve.open(self._get_user_shelf_path(user_id))

  def __del__(self):
    self.s.close()

  def __setitem__(self, key, value):
    self.s[key] = value
    self.s.sync()

  def __getitem__(self, key):
    return self.s[key]

  def __delitem__(self, key):
    del self.s[key]
    self.s.sync()

  @property
  def d(self) -> dict:
    return dict(self.s).copy()

  def get(self, key, default=None):
    return self.s.get(key, default=default)

  def wipe(self) -> None:
    self.s.clear()
    self.s.sync()


class t:
  @staticmethod
  def fs_object(type, name: str, *, hidden=False) -> FSObject:
    return normalize(
      {
        'type': type,
        'name': str(name),
        'hidden': bool(hidden),
      }
    )

  @staticmethod
  def dir(name: str, *contents: FSObject, hidden=False) -> Directory:
    return normalize(
      {
        **t.fs_object(type=Directory, name=name, hidden=hidden),
        'type': Directory,
        'directory': tuple(contents),
      }
    )

  @staticmethod
  def file(name: str, *, hidden=False) -> File:
    return normalize(
      {
        **t.fs_object(type=File, name=name, hidden=hidden),
        'type': File,
      }
    )

  @staticmethod
  def text_file(name: str, text: str, *, hidden=False) -> TextFile:
    return normalize(
      {
        **t.file(name=name, hidden=hidden),
        'type': TextFile,
        'text': str(text),
      }
    )

  @staticmethod
  def image_file(name: str, image_strpath: str, *, hidden=False) -> TextFile:
    return normalize(
      {
        **t.file(name=name, hidden=hidden),
        'type': ImageFile,
        'image_strpath': str(image_strpath),
      }
    )


def _is_file(f: FSObject) -> bool | None:
  if f['type'] in file_ts:
    return True
  if f['type'] is Directory:
    return False
  return None


def normalize(f: FSObject) -> FSObject:
  return merge_dicts(f, f['type']._DEFAULT, strict=False)


def normalize_path(path: str) -> str:
  path = path.replace('\\', '/')
  path = f'/{path}/'.replace('/./', '/')
  path = path.strip().strip('/').strip()
  return f'/{path}'


def path_basename(path: str) -> tuple[str, str]:
  """Return tuple(path-basename, basename)."""
  path = normalize_path(path).strip('/')
  path, paths = path[::-1].split('/', maxsplit=1)
  path = path[::-1]
  paths = [x[::-1] for x in paths]
  return '/'.join(paths), path


def fsobj_tostr(f: FSObject) -> str:
  if f['hidden']:
    return ''
    return f'{emoji_lookup[None]} <hidden item>'

  try:
    emoji = emoji_lookup[f['type']]
  except KeyError:
    emoji = emoji_lookup[None]

  return f'{emoji} {f["name"]}'


def auto_display(f: FSObject, path=None) -> str | hikari.Embed:
  isfile = _is_file(f)

  if isfile is None:
    raise ValueError('Invalid non-file, non-dir fsobject...?')

  if isfile:
    if f['type'] == TextFile:
      return text_file_embed(f, path)
    elif f['type'] == ImageFile:
      return 'not implemented - images'
    else:
      return "This file is corrupted (invalid f['type']?)"
  else:
    return directory_embed(f, path)


def split_path(path: str, *, normalize=True, remove_empties=True) -> list:
  if normalize:
    path = normalize_path(path)

  path = path.split('/')

  if remove_empties:
    path = [x for x in path if x]

  return path


def traverse(
  f: Directory, path: str, *paths: str, modify_last: dict | None | Null = None, append: bool = False
):
  """### Recursively traverse given path.

  Sorts the stumbled-on directories on the way there.

  ### Arguments:
  - modify_last=None  -> Return ONLY the last in line file
  - modify_last=Null  -> Return EVERYTHING but without the selected path (delete that item)
  - modify_last={...} -> Return EVERYTHING with that item, but modify it as follows: `it = {**it, **modify_last}`

  ### Raises:
  - `KeyError`: path is invalid
  - `TypeError`: tried to append to a non-directory.
  """
  path, *paths = split_path('/'.join((path, *paths)), normalize=True, remove_empties=True) or ['']

  if path == '' and not paths:
    traversed_one_step = f
    direct = []
  else:
    direct: list[FSObject] = list(f['directory'])
    for fso in direct:
      if fso['name'] == path:
        traversed_one_step = fso
        direct.remove(fso)
        break
    else:
      raise KeyError('invalid path')

  if paths:
    if modify_last is None:
      return traverse(traversed_one_step, *paths, modify_last=modify_last, append=append)
    else:
      return {
        **f,
        'directory': sorted(
          (*direct, traverse(traversed_one_step, *paths, modify_last=modify_last, append=append)),
          key=lambda x: x['name'],
        ),
      }
  else:
    if modify_last is None:
      return traversed_one_step
    if modify_last is Null:
      return {**f, 'directory': sorted(direct, key=lambda x: x['name'])}
    if isinstance(modify_last, dict):
      if append:
        if traversed_one_step['type'] != Directory:
          raise TypeError('Tried to append to a non-directory')
        traversed_one_step['directory'] = sorted(
          (*traversed_one_step['directory'], modify_last), key=lambda x: x['name']
        )
        if path == '':
          return traversed_one_step
        return {**f, 'directory': sorted((*direct, traversed_one_step), key=lambda x: x['name'])}
      else:
        modified = {**traversed_one_step, **modify_last}
        if path == '':
          return modified
        return {**f, 'directory': sorted((*direct, modified), key=lambda x: x['name'])}
    else:
      raise TypeError('modify_last must be None, tcr.Null or dict')


def test_traverse():
  directory = t.dir(
    '/',
    t.dir(
      'dir2',
      t.text_file('file1.txt', 'Text in the file1.txt'),
      t.text_file('file2.txt', 'Text in the file2.txt'),
    ),
    t.dir('aempty_dir'),
  )

  # console(traverse(directory, '/', modify_last={"hidden": True}))
  # console(traverse(directory, 'dir2', modify_last={"hidden": True}))
  console(traverse(directory, 'dir2', modify_last=t.dir('appended'), append=True))
  # console(traverse(directory, '', 'dir2', modify_last={"hidden": True}))
  # console(traverse(directory, 'dir2/file1.txt', modify_last=None))
  # console(traverse(directory, '/dir2/file1.txt', modify_last={"text": "fire in the hole"}))
  # console(traverse(directory, 'dir2/file1.txt', modify_last=Null))

  exit()

  test_traverse()


def directory_embed(directory: Directory, path: str) -> hikari.Embed:
  if directory['type'] != Directory:
    raise ValueError('Passed in dict is not a Directory type')

  item_texts: list[str] = []

  for fso in directory['directory']:
    match _is_file(fso):
      case None:
        raise ValueError(f"Invalid type: {fso['type']}")
      case _:
        if a := fsobj_tostr(fso):
          item_texts.append(a)

  return embed(
    f"Contents of {(a := normalize_path(path))}{'/' if a != '/' else ''}",
    '\n'.join(item_texts) or r'Nothing to see here ¯\_(ツ)_/¯',
    color=0x55ACEE,
  )


def text_file_embed(f: TextFile, path: str) -> hikari.Embed:
  return embed(
    f'Text contents of {path}',
    codeblock(f['text']),
  )


def test_db():
  udb0 = UserDB(0)
  udb1 = UserDB(1)

  udb0.wipe()
  udb1.wipe()

  console(udb0.d, udb1.d)

  udb0['uwu'] = {
    'type': Directory,
    'name': 'folder',
    'directory': [{'type': TextFile, 'name': 'file2.txt', 'text': 'Text in the file'}],
  }
  udb0['owo'] = {'type': TextFile, 'name': 'file.txt', 'text': 'Text in the file'}

  console(udb0.d, udb1.d)

  del udb0['uwu']

  console(udb0['owo'])
  console(udb0.user_id, udb1.user_id)
  console(udb0.d, udb1.d)

  exit()
