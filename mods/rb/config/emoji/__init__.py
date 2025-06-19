from _.config.models import CustomEmoji as E
from _.config.models import CustomEmojiStaticBase
from prelude import *

if TESTMODE:

	class CustomEmojiStatic(CustomEmojiStaticBase):
		fluff: E = "<:fluff:1372304836997021756>"

else:

	class CustomEmojiStatic(CustomEmojiStaticBase):
		fluff: E = "<:fluff:1372305099015061604>"
