import arc

from ..lang import LANG

OPTION_EPHEMERAL = arc.Option[bool, arc.BoolParams(**LANG.get_arc_command("/option.ephemeral"))]
OPTION_TO_FILE = arc.Option[bool, arc.BoolParams(**LANG.get_arc_command("/option.to_file"))]
OPTION_EXISTS_CHECK = arc.Option[bool, arc.BoolParams(**LANG.get_arc_command("/option.exists_check"))]

OPTION_CONFIRM_BOOL = arc.Option[bool, arc.BoolParams(**LANG.get_arc_command("/option.confirm_bool"))]
OPTION_CONFIRM_YES_DO_AS_I_SAY = arc.Option[str, arc.StrParams(**LANG.get_arc_command("/option.confirm_yes_do_as_i_say"), min_length=(_min_length := len("Yes, do as I say!")), max_length=_min_length)]
