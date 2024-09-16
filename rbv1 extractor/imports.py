class Reminder:
  unix = None  # The time of the reminder (int | str)
  text = None  # The text of the reminder (str)
  user = None  # Discord User ID (int | str)
  flag = 0  # Any reminders created before addition of the flags will have flags=0 after the reboot to the new version

  def __init__(self, unix, text, user, flag: int | None) -> None:
    self.unix = unix
    self.text = text
    self.user = user
    self.flag = flag

  def __str__(self) -> str:
    return f'**{self.text}** (<t:{self.unix}:R>)'

  def __repr__(self) -> str:
    return f'/{self.text}/'