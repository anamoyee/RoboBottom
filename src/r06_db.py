from r05_embed import *

if True:  # DB Hints

  class U(TD):
    r: list[Reminder]

  U.defaults = {
    'r': list,
  }

  class V(TD):
    revolution: int

  V.defaults = {
    'revolution': int,
  }

  class G(TD): ...


if True:  # DB Types

  class Database(tcr.ShelveDB):
    directory = DB_USERS_PATH
    defaults = U.defaults

    def append_reminder(self, rem: Reminder) -> None:
      """Append a reminder object to that user's reminder list in their database.

      May raise TextErrpondError.
      """
      r = self['r']

      if len(r) >= S.REMINDER_LIST_MAX_TOTAL_REMINDERS_PER_USER:
        raise TextErrpondError("How??", f'You somehow reached the user reminder limit (`{S.REMINDER_LIST_MAX_TOTAL_REMINDERS_PER_USER}`)...')

      r.append(rem)
      r = sorted(r, key=S.SORTKEY)
      self['r'] = r

    @classmethod
    def iter_all(cls) -> t.Iterator[tuple[str, 'U | Database']]:
      return super().iter_all()

  class _VersionDatabaseType(tcr.ShelveDB):
    directory = DB_VERSION_PATH
    defaults = V.defaults

    def drop_db(self) -> None:
      self.clear()

    @classmethod
    def iter_all(cls) -> t.Iterator[tuple[str, 'V | _VersionDatabaseType']]:
      return super().iter_all()

    def inc_revolution(self) -> None:
      self['revolution'] = self['revolution'] + 1

  class _GlobalDatabaseType(tcr.ShelveDB):
    directory = DB_GLOBAL_PATH.parent

    @classmethod
    def iter_all(cls) -> t.NoReturn:
      raise RuntimeError('You cannot use iter_all() on the global database due to the internal folder structuring.\nIt does not even make sense to do it - there is only one global database.')

    def drop_db(self) -> None:
      self.clear()


if True:  # DB Declarations
  VDB: V | _VersionDatabaseType = _VersionDatabaseType(VERSION.replace('.', '_'))
  GDB: G | _GlobalDatabaseType = _GlobalDatabaseType(DB_GLOBAL_PATH.name)
