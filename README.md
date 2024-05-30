### This is python 3.11 version, for ~~3.12~~ (edit: i guess it will still support 3.11...) rewrite go to [the main branch](https://github.com/anamoyee/RoboBottom/tree/main), keep in mind it's still a work in progress! It may not be functional yet, but I will post any updates there from now on


# RoboBottom
A clone/remake of **[RoboTop](https://robotop.xyz)**'s reminder system. RoboTop was originally made by **[Colon](https://gdcolon.com)** <img style="width: 15px; height: 15px;" src="https://cdn.discordapp.com/emojis/1132968267963715634.webp?size=64&name=fluff&quality=lossless"></img>. I remade the *reminders* part of that bot because of its shutdown on August 12th 2023. RIP RoboTop, You will be missed!

## How do I host it myself?
1. Install **[Python](https://www.python.org/downloads/)** and add it to PATH during instalation.
2. Install python modules using the following command in the main project's directory.
```
pip install -r requirements.txt
```
3. Go to `settings.py` and change your settings accordingly.
4. Create an application on **[Discord Developer Portal](https://discord.com/developers/applications)** and grant it all priviliged gateway intents (I don't really know if they are needed but I just always grant them and I don't know if it will break something if it's not grantetd).
5. The bot will try to find a file called `TOKEN.txt` up to two directories away (in cwd, parent & parent of parent). Create it and populate it with the bot's token.
6. Run the bot with the following command
```
python robobottom.py
```

# Database Logistical Notes
(You might want to know this if you want to host the bot yourself)
<details>
<summary><b>Windows</b></summary>
A <code>db</code> folder is created in the current directory which holds all reminder data.
</details>
<details>
<summary><b>Non-Windows</b></summary>
it tries to go back two directories and create a <code>RoboBottomDB</code> folder there.
</details>
(Uh... and actually that's not really a database, it's just a 'shelf' aka a python dictionary that persists between relaunches, made with `shelve` module and that folder is where the shelve files are stored)

## Contact
If you have any questions contact me on discord `@thecreatorrrr`\
If i change my username for some reason (or discord again fucks up the username system) here's my id `<@507642999992352779>`

# Todo
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
