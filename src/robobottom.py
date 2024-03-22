__import__('os').system('pip install --upgrade tcrutils') if 't' in __import__('sys').argv else ''  # fmt: skip

from r13_events import *

if __name__ == '__main__':
  if S.BANNER is not None:
    print(
      '\n'.join(f'  {S.BANNER_COLORS[1]}{"".join([(char if i != S.BANNER_COLORS[0] else f"{char}{S.BANNER_COLORS[2]}") for i, char in enumerate(line)])}' for line in S.BANNER.split('\n')) + '\n'
    )

  if testmode():
    tcr.alert('Running in testmode', printhook=c.log)

  if S.DEFAULT_EANBLED_GUILDS:
    tcr.alert(f'Running with DEG: {len(S.DEFAULT_EANBLED_GUILDS)}', printhook=c.log)

  BOT.run(status=S.STATUS, activity=S.ACTIVITY)
