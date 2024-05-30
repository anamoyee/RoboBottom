from r10_components import *

TASKS: list[arc.utils.CronLoop | arc.utils.IntervalLoop] = []


def register_task(task):
  TASKS.append(task)
  return task


@register_task
@arc.utils.interval_loop(seconds=S.REMINDER_TASK_INTERVAL_SECONDS)
async def task_reminder(*, bot: hikari.GatewayBot, acl: arc.GatewayClient) -> None:
  for _, db in Database.iter_all():
    for rem in db['r']:
      if rem.expired():
        await rem.send(bot)
        rem.remove_from_db()


@register_task
@arc.utils.cron_loop(S.BACKUP_CRON)
async def task_backup():
  c('Backup task executed')
