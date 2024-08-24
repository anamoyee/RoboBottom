from r00_imports import *


def print_banner(printhook: Callable[[str], None] = print) -> None:
  """Print the RoboBottom banner to the console, if S.BANNER is not None, else do nothing."""

  if R.S.BANNER is None:
    return

  banner_text = R.S.BANNER.read_text().strip()
  banner_text = [line for line in banner_text.split('\n') if not line.strip().startswith('# COMMENT #')]
  banner_text = ('\n'.join(banner_text)).strip().split('\n')
  banner_text = [f'  {eval(f"f{x!r}", globals().copy(), {**R.__dict__, "BC": R.S.BANNER_COLORS})}' for x in banner_text]
  banner_text = [Style.RESET + x for x in banner_text]
  banner_text = f'{tcr.NEWLINE.join(banner_text)}\n'

  printhook(banner_text)
