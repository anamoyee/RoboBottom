## This is the main branch which contains **UNIFNISHED** v2 version. To get the fully functional (although kinda janky and it-really-required-this-rewrite version go to [the archive branch](https://github.com/anamoyee/RoboBottom/tree/archive).

# RoboBottom
A clone/remake of **[RoboTop](https://robotop.xyz)**'s reminder system. RoboTop was originally made by **[Colon](https://gdcolon.com)** <img style="width: 15px; height: 15px;" src="https://cdn.discordapp.com/emojis/1132968267963715634.webp?size=64&name=fluff&quality=lossless"></img>. I remade the *reminders* part of that bot because of its shutdown on August 12th 2023. RIP RoboTop, You will be missed!

## How do I host it myself?
1. Install **[Python 3.11](https://www.python.org/downloads/)** and add it to PATH during instalation.
  - On Linux you can use **[Parafoxia](https://github.com/parafoxia)**'s **[Python Install Scripts](https://github.com/parafoxia/python-scripts)**
  - On Windows use the installer from **[Python Official Website](https://www.python.org/downloads/)** (or the Microsoft Store bleh)
2. Install python modules using the following command in the main project's directory. (`pip3.11`/`pip3` on linux)
```
pip install -r requirements.txt
```
1. Create an application on **[Discord Developer Portal](https://discord.com/developers/applications)** and grant it all priviliged gateway intents.
2. The bot will try to find a file called `TOKEN.txt` up to two directories away (in cwd, parent & parent of parent). Create it and populate it with the bot's token.
3. Run the bot with the following command (`python3`/`python3.11` on linux)
```
python src/robobottom.py
```

> [!IMPORTANT]
> You may use Python 3.12 if it works for you however i cannot guarantee it. Please use Python 3.11 if possible.

## Contact
If you have any questions contact me on discord `@anamoyee`\
If i change my username for some reason (or discord again fucks the username system up) here's my id `<@507642999992352779>`

# Todo v3
- [ ] finish help.py plugin and its commands
- [ ] Switch settings to pydantic
- [ ] Switch Reminder to pydantic
- [ ] Reminder archive: New list (.) toggle/switch to view expired reminders (& search)
  - [ ] Fuck timeout: add reminders to archive and instead of timeout bool whether it was triggered or not, then notify the user if there are any reminders in the archive which have not been triggered
- [ ] make attachments fallback to a file containing a list of links with an explaination if any failed to attach (hikari.HTTPError when sending)
- [ ] make banner not use eval (tcr.execute)
- [ ] seamless #year channel integration (but in DMs) and it reminds you of the events.
  - Input made by giving an exact date of the event with year & a recursion string of exactly 1 year
- [ ] recursive strings
- [ ] make settings display and work
- [ ] make reminder `text` with {placeholders}
- [ ] make reminder `time` with {placeholders}
- [ ] (?) do something with loops not stopping on shutdown
  - And what's wrong with shutting down? it adds terminated tasks
- [ ] Finish validators
- [ ] Do a grep for `TODO` and impl all of them
- [ ] Look through the previous todos and find any worthy checkboxes (either checked or unchecked since like, this is a v2) and maybe add them to this list
- [x] `^` prefix to count time from the reminder delivery time instead of current time
  - [x] Round the preceived delivery time to the nearest minute, **up or down**!
- [x] add "from 4h ago" to the reminder footer
- [x] r13_slash.py:181 impl slash command ids
- [x] in-discord error logging & add the following error handlers
  - [x] arc handler (research how to) - replicate the default one to enable in-discord logging
    - This should also show more detail on dev commands
  - [x] GMCE handler (kind of replicate arc, such that it responds with :x: and logs errors)
- [x] handle bot being blocked (if send fails with the block error add timeout)
- [x] handle view & cancel attachments issue (not using safemode)
  - [x] view
  - [x] cancel
- [x] use arc hooks
- [x] when viewing or receiving a reminder, if the message failed to send, send two files: reminder raw as if it was exported (json) ans the reminder text (txt) with at the bottom of the text files all the attachment URLs if any
- [x] finish /backup import
- [x] add dev cmds:
  - [x] add `$users` (get amount of unique users using the bot)
  - [x] add `$servers` (get amount of servers using the bot)
  - [x] add `$get` for getting the raw reminder ansi printed
- [x] make a `fuck` command that undos the latest reminder schedule
- [x] make basic stuff work
- [x] make attachments visible when viewing reminder
- [x] make attachments visible when viewing list of reminders (🗃📝)
- [x] fix revcounter
- [x] MAKE STATS LIKE: FIRST INTERACTED WITH THE BOT.
- [x] [EXPORT] Add option to backup your reminders to a file and to load them later.
- [x] Add to the reminder: `This reminder was sent ... too late`.

# Todo v2
- [X] Add vaidators for BANNER & BANNER_COLORS
- [X] Add default enabled guilds to guilds
- [X] **!!! SECURE dev commands.**
- [ ] Priority system
  - [ ] priority overrides (option for users to choose diff priority than time-based)
  - P1 and `P1 \>\> ` highlight for reminders that have been set for **1 year or more**
  - P2 and `P2 \> ` highlight for reminders that have been set for **1 month or more**
  - P3 and `P3 ` highlight for reminders that have been set for **1 week or more**
  - No priority-highlight for other reminders
- [ ] `n*` syntax: `3*1h test` -> do the same as typing `1h test` 3 times
- [ ] Validate settings value with SETTING_VALID_SONMETHING_CHARACTERS
- [ ] When responding to creating a reminder: "Sure! I'll remind you in..." add setting to append something like (it's idx=...)
  - For example: `Sure! I'll remind you in 1 hour. (id=19)`
- [ ] Add a setting to add a view with buttons like "No, wait, cancel" or "Preview" to the "Sure! i'll remind you in..." message
  - [ ] Make them disappear (`.edit(components=[])`) after a while
- [ ] Entering "rubrub" or "rub" rescue whenever the `.` message fails to load
  - List the rem amount
  - Show bottom-most (-1) rem
  - Suggest cancelling -1 rem
  - Suggest reporting bug
- [ ] image support
- [ ] integrate the Melanie announcements to robobottom:
  - Attention all (1) passengers... Wilford Industries wishes you a good morning. The temperature outside is {get_temperature()} degrees Celsius. As we enter the Yukon Territory of the former Canada, we remind you, for your personal safety, be prepared to brace. We are {get_formated_days_since_birth()} from departure. At the tone, the exact time will be 0800 hours.
- [ ] add a ".then()" functionality. When defining you can specify two reminders or more (with some new separator, very hard to accidentally type) or some other way maybe to have a 'next' button which schedules the reminder net in line if any for example:
5m ładowanie$$$1h unładowanie
- [ ] **Add stats** (viewable for the user maybe)
- [ ] message id editing (add a message id property to Reminder: `message_id: int | None`)

# Todo v1 (archive)
- [x] `/remind` for servers
- [x] Update /help msg to include /remind in servers
- [x] SORT the `.` list to be from furthest to closest reminders
- [x] lowercase the time bruh because `2H` doesnt work
- [ ] Flags/prefixes/idks
  - [x] Important (`!` prefix), mentions the user
  - [ ] Recurring (`&` prefix), doesnt cancel after remindion
  - [x] Hidden (`#`), its text doesnt show in `.` list and when canceling
    - [ ] Ability to pause hidden reminders
  - [x] DISPLAY THE PREFIXES IN THE `.` LIST!!! (`! &`)
- [ ] `defer` & `undefer`
- [ ] Folders with indentation
- [x] If message has only delay part and responds to sth delay that thing the amount
- [x] Add battery indicators in the activity text
- [ ] Add more time formats:
  - [ ] `(?:{days}d + )?HH:MM:SS`
  - [x] `@HH:MM:SS` (not relative, for example 22:00 will count current hour and subtract it from the selected @hour, then it will )
  - [x] When user supplies `{x}h{y}` (without the m) make it implicit since it directly follows the hours
- [ ] Add support for displaying images (may be scrapped because of recent discord caveats)
- [ ] !!! **Select menu components (with modal +new reminder)**
- [x] Add confirmation to /delhistory
- [ ] add buttons on Rescue! and Successfully canceled reminder to reschedule the reminder for `5m` `15m` `1h` `6h` `24h`
- [x] increase max message length
- [x] fix too long message resulting in invalid syntax
- [x] Limit the length of displayed message (EMBEDS._list) but keep the text intact
- [x] !!! **Rewrite the scheduling reminder, take content and rewrite the actual delay scheisse**
  - [x] ! TimeExp binary joiner
- [ ] user settings and default settings (default dict)
- [ ] set alarm with termux (or notif)
- [x] remove useless @ prefix since it can be detected with :
- [x] make "remidner cancelled" embed more like it was back in robotop
- [ ] Update the `/help syntax` command to account for t:im:e, d:at:e & weekdays syntaxes
- [ ] Add setlocale support (dep: usersettings from one of previous checkmarks)
- [ ] make it possible to have image attachments but notify if the user has set the reminder time to over the discords limit
- [x] **@ SYNTAX BUT FOR DAYS bruh why didnt i add it already????**
- [ ] Fix uncaught exceptions when bot takes too long to respond to an interaction
- [ ] cancelling by name (`cancel <name>` instead of `cancel <number>`)
- [x] Add reminder pages
- [x] Set the custom status (Not "watching")
- [x] Make "Your reminders" NOT reply-actionable
- [x] Filter last backtick if number of them is odd
- [ ] quick reschedule buttons
- [ ] what if you block robo and it sends a reminder?
- [ ] pass each message through /#{1,3} (.*)/ and replace with \1
- [ ] **reminder content editing**
- [x] make the RoboBottom important @mention be with heading 1 when sending (`# <@id>`)
- [x] filter triple backticks from list and replace with '''
- [ ] After db update, edit the latest list_ message for that user
- [ ] `/\. ?(?:query syntax)/`
- [ ] make the fucking recursive with \<first_delay>&\<recursive_delay> syntax'
- [ ] tasks (like nieprzygotowania, osobne kategorie):
  - [ ] `tasks view <category>` (`t v <category>`) for example (`t v np`)
- [ ] Relative rescheduliong reply action (`^16h` - instead of 16h from now, make it 16 hours from when that reminder expired)
- [x] Add polish weekday options
- [ ] add revolution counter in /botstatus (`tcr.nth()`)
- [ ] ~~Make `v @cat` syntax~~ make `@db` syntax
- [ ] Robo bottom personal DBs, file system like, reuse from terminal
- [ ] make a "a red spy is in the base" Easter egg that no one will ever find in robobottom
- [ ] add edit text with modal onto embed view

~~<style>s{color: crimson;} b,strong{text-decoration:underline}</style>~~
<!-- I am MEGUMIN the greatest mage among crimson demons and wielder of EXPLOSION MAGIC -->
~~<style>p, li{font-family: "Hubot Sans Bold"; font-size: 17px}</style>~~
~~<style>code, pre{font-family: Consolas}</style>~~
~~<style>code{background-color: #271a45; border-radius: 4px; padding: 2px; padding-left: 5px; padding-right: 5px;}</style>~~
