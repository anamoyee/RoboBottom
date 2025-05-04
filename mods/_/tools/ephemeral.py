import hikari


def ephemeral_from_bool(is_ephemeral: bool, /) -> hikari.MessageFlag:
	return hikari.MessageFlag.EPHEMERAL if is_ephemeral else hikari.MessageFlag.NONE


def ephemeral_from_bool_flags(is_ephemeral: bool, /, *, or_with: hikari.MessageFlag = hikari.MessageFlag.NONE) -> hikari.MessageFlag:
	return {"flags": ephemeral_from_bool(is_ephemeral) | or_with}
