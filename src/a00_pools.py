import typing as t

if True:  # Functional
  if True:  # Types

    class AliasesDict(dict):
      def __call__(self, __key: str) -> list[str]:
        return [__key, *self[__key]]

      def get_n_shortest(self, key: str, n: int = 5) -> list[str]:
        return sorted(self(key), key=lambda x: len(x))[:n]

  DM_CMD_ALIASES: AliasesDict[str, t.Iterable[str]] = AliasesDict(
    {
      'list': ('.', 'ls', 'l', 'reminders', 'rems', 'list reminders', 'list rems', 'listreminders', 'listrems'),
      'cancel': ('c', 'cancel reminder', 'cancel rem', 'cancelreminder', 'cancelrem'),
      'view': ('v', 'view reminder', 'view rem', 'viewreminder', 'viewrem'),
      'del': ('delete', 'delthis', 'del this', 'delete this', 'deletethis', 'remove', 'removethis', 'removethis'),
      'fuck': ('fk', 'fucjk', 'shit', 'waitno', 'wait no', '💩'),
      'wipe': (),
    }
  )
