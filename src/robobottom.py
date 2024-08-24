from r14_events import *

if __name__ == '__main__':
  if True:  # Print banner
    print_banner()

  if testmode():
    tcr.alert('Running in testmode', printhook=c.log)

  if S.PRINT_REVOLUTION:
    VDB.inc_revolution()
    c.log('On the eve of our %s revolution...' % tcr.nth(VDB['revolution']))

  if S.DEFAULT_EANBLED_GUILDS:
    tcr.alert(f'Running with DEG: {len(S.DEFAULT_EANBLED_GUILDS)}', printhook=c.log)

  if True:  # Load ./plugins
    plugins_folder = p.Path(__file__).parent / 'plugins'
    _cwd = os.getcwd()
    os.chdir(plugins_folder.parent)
    ACL.load_extensions_from(plugins_folder.name)
    os.chdir(_cwd)

  BOT.run(status=S.STATUS, activity=S.ACTIVITY)
