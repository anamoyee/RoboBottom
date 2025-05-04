from prelude import *

from ..config import S
from ..models import AnimalC


class Guild(ZooBM):
	stashed_animal: AnimalC | None = None
