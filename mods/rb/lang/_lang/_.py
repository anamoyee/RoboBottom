from mods._.config import S as S1

_ = {
	**{  # slash commands
		**{  # /remind
			"/.remind.name": "remind",
			"/.remind.description": "Set a reminder!",
			"/.remind:text.name": "text",
			"/.remind:text.description": "The expression that is evaluated to create a reminder, see /help for more info",
			"/.remind:here.name": "here",
			"/.remind:here.description": "Later send the reminder in this channel instead of your primary channel (your DMs by default).",
		},
		**{  # /peek
			"/.peek.name": "peek",
			"/.peek.description": "Peek at a few of the most recent delivered reminders in a given channel (your DMs by default).",
			"/.peek:amount.name": "amount",
			"/.peek:amount.description": "The amount of reminders to peek at (max 10 due to discord limitations).",
			"/.peek:channel.name": "channel",
			"/.peek:channel.description": "The channel to peek at (your DMs by default).",
			"/.peek:channel.invalid_channel": f"{S1.NO} The channel you provided doesnt seem to exist or is unsuitable for this action...",
			"/.peek.no_embeds": f"{S1.NO} No embeds were found in the selected channel...",
			"/.peek.failed_to_send": f"{S1.NO} Something went wrong while trying to send the message...\n-# (Do you have a bunch of large embeds? We might be hitting the discord limitation)",
		},
	},
}
