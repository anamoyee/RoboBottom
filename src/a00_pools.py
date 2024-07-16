import typing as t

if True:  # Functional
  if True:  # Types

    class AliasesDict(dict):
      def __call__(self, __key: str) -> list[str]:
        return [__key, *self[__key]]

  DM_CMD_ALIASES: AliasesDict[str, t.Iterable[str]] = AliasesDict(
    {
      'list': ('.', 'list', 'ls', 'l', 'reminders', 'rems', 'list reminders', 'list rems', 'listreminders', 'listrems'),
      'cancel': ('c', 'cancel', 'cancel reminder', 'cancel rem', 'cancelreminder', 'cancelrem'),
      'view': ('v', 'view', 'view reminder', 'view rem', 'viewreminder', 'viewrem'),
      'del': ('delete', 'delthis', 'del this', 'delete this', 'deletethis', 'remove', 'removethis', 'removethis'),
      'fuck': ('fk', 'fucjk', 'shit', 'waitno', 'wait no', '💩'),
    }
  )
