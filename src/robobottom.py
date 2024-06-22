from r14_events import *


def print_banner():
  banner_text = S.BANNER.read_text().strip()
  banner_text = [line for line in banner_text.split('\n') if not line.strip().startswith('# COMMENT #')]
  banner_text = ('\n'.join(banner_text)).strip().split('\n')
  banner_text = [f'  {eval(f"f{x!r}", globals().copy(), {**locals(), "BC": S.BANNER_COLORS})}' for x in banner_text]
  banner_text = [Style.RESET + x for x in banner_text]
  banner_text = f'{tcr.NEWLINE.join(banner_text)}\n'

  print(banner_text)


if __name__ == '__main__':
  if S.BANNER is not None:
    print_banner()

  if testmode():
    tcr.alert('Running in testmode', printhook=c.log)

  if S.PRINT_REVOLUTION:
    VDB.inc_revolution()
    c.log('On the eve of our %s revolution...' % tcr.nth(VDB['revolution']))

  if S.DEFAULT_EANBLED_GUILDS:
    tcr.alert(f'Running with DEG: {len(S.DEFAULT_EANBLED_GUILDS)}', printhook=c.log)

  BOT.run(status=S.STATUS, activity=S.ACTIVITY)
