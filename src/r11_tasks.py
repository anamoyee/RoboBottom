from r10_components import *

TASKS: list[arc.utils.loops._LoopBase] = []


def register_task(task):
  TASKS.append(task)
  return task


@register_task
@arc.utils.interval_loop(seconds=S.REMINDER_TASK_INTERVAL_SECONDS, run_on_start=False)
async def task_reminder() -> None:
  for _, db in Database.iter_all():
    for rem in db['r']:
      if rem.expired():
        await rem.send()
        rem.remove_from_db()


@register_task
@arc.utils.cron_loop(S.BACKUP_CRON, timezone=S.GLOBAL_TIMEZONE)
async def task_backup():
  c('Backing up all databases...')
  backed_up_to = backup_all_databases()
  c.log(f'Backed up to {backed_up_to}')
