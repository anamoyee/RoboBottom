from r02_settings import S

pass
from r01_types import *

TOKEN = tcr.get_token('TOKEN.txt', depth=3)  # 3-1 = 2 counting src/
UPTIME = tcr.Uptime()
VERSION = S.MAJOR_VERSION_TEMPLATE % p.Path('VERSION.txt').read_text().strip()
TIMESTR = tcr.TStr(tzinfo=S.GLOBAL_TIMEZONE, splitter='!', fix_timezone=True)
TESTMODE = (os.name == 'nt') if S.FORCE_TESTMODE is None else S.FORCE_TESTMODE

DB_USERS_PATH = S.DB_DIRECTORY / 'users'
DB_USERS_PATH.mkdir(exist_ok=True, parents=True)  # fmt: skip
DB_VERSION_PATH = S.DB_DIRECTORY / 'version'
DB_VERSION_PATH.mkdir(exist_ok=True, parents=True)  # fmt: skip
DB_GLOBAL_PATH = S.DB_DIRECTORY / 'global'
DB_GLOBAL_PATH.mkdir(exist_ok=True, parents=True)  # fmt: skip

SETTINGS_PAGE_KEYS: list[str] = [x.name for x in UserSettings.__attrs_attrs__]
SETTINGS_VALUE_ALLOWED_CHARACTERS: str = string.ascii_letters + string.digits + '_- '
SETTINGS_VALUE_MAX_LENGTH: int = 100
SETTINGS_LABEL_LOOKUP = {
  None: 'Change Setting',
  'timezone': 'Set Timezone',
}
