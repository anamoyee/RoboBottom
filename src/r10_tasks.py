from r09_components import *


@tasks.task(s=S.REMINDER_TASK_INTERVAL_SECONDS, wait_before_execution=True)
async def reminder_task():
  users_dbdir = get_db('u', tcr.Null)

  listdir = os.listdir(users_dbdir)

  timedottime = time.time()

  for id in listdir:
    with shelve.open(users_dbdir / id / id) as shelf:
      shelf.setdefault('r', [])

      for reminder in shelf['r']:
        reminder: Reminder

        if timedottime >= reminder.unix:
          if S.DEBUG_REMINDERS_ON_SEND:
            c.debug(f'Reminder sent to {reminder.user}: {reminder.text} ({reminder.tstr})', quoteless=True)
          await trigger_reminder(reminder, delete=True)
