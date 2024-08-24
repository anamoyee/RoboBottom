import arc
import hikari
from r00_imports import *


async def dev_only_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is not authorised to run this dev command. Notifies user by responding."""
  if ctx.author.id not in R.S.DEV_IDS:
    await ctx.respond(**R.RESP.not_dev())
    return arc.HookResult(abort=True)
  return arc.HookResult()


async def bannable_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is banned. Notifies user by responding."""
  if ctx.author.id in R.GDB['banned']:
    await ctx.respond(**R.RESP.banned())
    return arc.HookResult(abort=True)
  return arc.HookResult()


async def dms_only_hook(ctx: arc.GatewayContext) -> arc.HookResult:
  """Aborts execution if user is not in a DM channel."""
  if ctx.guild_id is not None:
    await ctx.respond(**await R.RESP.must_use_dms(user_id=ctx.author.id))
    return arc.HookResult(abort=True)
  return arc.HookResult()


def do_as_i_say(func: Callable):
  """Ensures the "Yes, do as I said!" confirmation as a slash cmd argument."""

  @wraps(func)
  async def wrapper(*args, **kwargs):
    if not R.did_as_i_said(kwargs['doasisay']):
      await args[0].respond(f'{R.S.NO} You did not type the phrase correctly, make sure to use this command carefully!', flags=hikari.MessageFlag.EPHEMERAL)
      return None
    return await func(*args, **kwargs)

  return wrapper


DOASISAY_OPTION = arc.Option[str, arc.StrParams('Type exactly "Yes, do as I say!" to confirm this potentially dangerous action', min_length=17, max_length=17)]
