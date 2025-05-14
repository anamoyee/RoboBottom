from prelude import *

from ..models import CustomEmoji as E
from ..models import CustomEmojiStaticBase

if TESTMODE:

	class CustomEmojiStatic(CustomEmojiStaticBase):
		fluff: E = "<:fluff:1372304836997021756>"

else:

	class CustomEmojiStatic(CustomEmojiStaticBase):
		fluff: E = "<:fluff:1372305099015061604>"
