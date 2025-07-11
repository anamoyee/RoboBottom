from _.langtools import *

_ = {
	**{  # slash commands
		**{  # /botstatus
			"/.botstatus.name": "botstatus",
			"/.botstatus.description": "View some (partially made-up) details about the bot",
		},
		**{  # /settings
			"/.settings.name": "settings",
			"/.settings.description": "Modify settings for your profile",
		},
		**{  # /profiles
			"/.profiles.name": "profiles",
			"/.profiles.description": "View your profiles, or switch to a different one",
			"/.profiles:profile.name": "profile",
			"/.profiles:profile.description": "A specific profile to view",
		},
	},
	**{  # slash command options
		"/option.ephemeral.name": "ephemeral",
		"/option.ephemeral.description": "Hide the result?",
		"/option.to_file.name": "to_file",
		"/option.to_file.description": "Save the result as a file?",
		"/option.exists_check.name": "exists_check",
		"/option.exists_check.description": "Check if exists, instead of implicitly creating setdefault-style when missing?",
		"/option.confirm_bool.name": "confirm",
		"/option.confirm_bool.description": "You are about to do something potentially harmful. Confirm here to continue.",
		"/option.confirm_yes_do_as_i_say.name": "confirm",
		"/option.confirm_yes_do_as_i_say.description": "You're about to do something potentially harmful. To continue type in the phrase 'Yes, do as I say!'",
	},
	**subclass_values(  # http codes
		lambda tup: f"{tup[0]} **`{tup[1]}` {tup[2]}**: {tup[3]}",
		**subclass_items(
			lambda k, v: ((S.NO, _code_n := 403, "Forbidden", v), f"http.{_code_n}.{k}")[::-1],
			**{
				"/command": "You do not have permission to use this command.",
				"button": "You do not have permission to press this button.",
				"select": "You do not have permission to press this select menu.",
				"permbanned": "Your account has been permanently banned from using this bot as per the bot's [terms of service](https://documents.anamoyee.pages.gay/robobottom/tos).",
			},
		),
	),
}
