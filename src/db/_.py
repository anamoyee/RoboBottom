from tcrutils import ShelveDB

from ..settings import S


class User(ShelveDB):
	directory = S.DATABASE.ROOT_DIR / "users"


