DEFAULT_ENABLED_GUILDS = () # Leave as empty tuple for slash commands to show up everywhere
#   1145433323594842166,
# )

DEV_ID    = 507642999992352779
DEV_GUILD = 1145433323594842166

VERSION = '3.0.1'

class ALIASES:
  LIST = ['.', 'list', 'reminders', 'rems']
  WIPE = ['clear', 'wipe', 'deleteall', 'cancelall']


class LIMITS:
  REMINDER         = 24 # Reminders
  MINIMAL_DURATION = 15 # Seconds

class RUNNING_ON:
  LINUX   = 'My phone [*permanent hosting*]'
  WINDOWS = 'My PC [*debugging bench*]'

STATUS = "Used in DMs"

USE_TEST_TOKEN_IF_AVAILABLE = True