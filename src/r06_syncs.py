from r05_embed import *


def get_db(db: Literal['u', 'v', 'g'], id: str | int | None | tcr.Null = None) -> p.Path:
  match db:
    case 'u':
      if id is None:
        raise TypeError("You must specify id for db='u' unless you want the entire directory, then specify id=tcr.Null")
      if id is tcr.Null:
        return DB_USERS_PATH
      else:
        if not isinstance(id, str | int):
          raise TypeError('id must be str or int')

        if not str(id).isalnum():
          raise ValueError('id must be alphanumeric (or int)')

        strid = str(id)
        (DB_USERS_PATH / strid).mkdir(exist_ok=True)
        return DB_USERS_PATH / strid / strid
    case 'v':
      if id is not None:
        raise TypeError('id is not supported in version/global')
      v = VERSION.replace('.', '_')
      (DB_VERSION_PATH / v).mkdir(exist_ok=True)
      return DB_VERSION_PATH / v / v
    case 'g':
      if id is not None:
        raise TypeError('id is not supported in version/global')
      return DB_GLOBAL_PATH
    case _:
      raise RuntimeError('Invalid db, choose "u", "v" or "g".')


def testmode(*, dash=True) -> str:
  return f'{" - " if dash else ""}Testmode' if TESTMODE else ''


def author_dict(
  who: hikari.OwnUser | hikari.User | None = None,
  url: str | None = None,
  *,
  displayname: bool = False,
) -> dict:
  if who is None:
    who = BOT.get_me()

  dick = {
    'name': who.username if not displayname else tcr.getattr_queue(who, 'display_name', 'username'),
    'icon': who.avatar_url or who.default_avatar_url,
  }

  if url:
    dick.update({'url': url})

  return dick


def random_sure() -> str:
  return rng.choice(S.RANDOM_SURES)


if True:  # Reminder Syncs

  def add_reminder_to_user(reminder: Reminder) -> None:
    """Append reminder to user's remlist and sort it."""
    with shelve.open(get_db('u', reminder.user)) as shelf:
      shelf.setdefault('r', [])
      shelf['r'] = sorted([reminder, *shelf['r']], key=S.SORTKEY)

  def delete_reminder_by_idx(user_id: int, idx: int) -> None:
    """Removes user's reminder by its index. If not found, raise IndexError. Sort the remlist."""
    with shelve.open(get_db('u', user_id)) as shelf:
      shelf.setdefault('r', [])
      shelf['r'] = sorted([x for i, x in enumerate(shelf['r']) if i != idx], key=S.SORTKEY)

  def delete_reminder_by_uuid(user_id: int, uuid: int):
    with shelve.open(get_db('u', user_id)) as shelf:
      shelf.setdefault('r', [])
      shelf['r'] = sorted([x for x in shelf['r'] if x.uuid != uuid], key=S.SORTKEY)

  def delete_reminder_by_reminder(reminder: Reminder) -> None:
    delete_reminder_by_uuid(reminder.user, reminder.uuid)
