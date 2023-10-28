# RoboBottom
A remake of **[RoboTop](https://robotop.xyz)**'s reminder system. RoboTop was originally made by **[Colon](https://gdcolon.com)** <img style="width: 15px; height: 15px;" src="https://cdn.discordapp.com/emojis/1132968267963715634.webp?size=64&name=fluff&quality=lossless"></img>. I remade the *reminders* part of that bot because of its shutdown on August 12th 2023. RIP RoboTop, You will be missed!

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
- [x] ~~Tell when would cancelled reminder remind on cancelation~~ *scrapped because it looked ugly*
- [x] lowercase the time bruh because `2H` doesnt work
- [ ] Flags/prefixes/idks
  - [x] Important (`!` prefix), mentions the user
  - [ ] Recurring (`&` prefix), doesnt cancel after remindion
  - [x] Hidden (`#`), its text doesnt show in `.` list and when canceling
    - [ ] Ability to pause hidden reminders
  - [ ] Text == `r` | `repeat` => text = (text of user's last trigered reminder)
  - [x] DISPLAY THE PREFIXES IN THE `.` LIST!!! (`! &`)
- [ ] `defer` & `undefer`
- [ ] Folders with indentation
- [ ] If message has only delay part and responds to sth delay that thing the amount
- [x] Add battery indicators in the activity text
- [ ] Add more time formats:
  - [ ] `(?:{days}d + )?HH:MM:SS`
  - [ ] `@HH:MM:SS` (not relative, for example 22:00 will count current hour and subtract it from the selected @hour, then it will )
  - [ ] When user supplies `{x}h{y}` (without the m) make it implicit since it directly follows the hours
- [ ] Add support for displaying images (may be scrapped because of recent discord caveats)
- [ ] !!! **Select menu components (with modal +new reminder)**
- [ ] Add confirmation to /delhistory
- [ ] add buttons on Rescue! and Successfully canceled reminder to reschedule the reminder for `5m` `15m` `1h` `6h` `24h`
- [x] increase max message length
- [ ] fix too long message resulting in invalid syntax
- [ ] Limit the length of displayed message (EMBEDS._list) but keep the text intact
- [ ] !!! **Rewrite the scheduling reminder, take content and rewrite the actual delay scheisse**
  - [ ] & TimeExp binary joiner
- [ ] user settings and default settings (default dict)
- [ ] set alarm with termux (or notif)
- [ ] remove useless @ prefix since it can be detected with :
- [ ] replace(' + ', '!') (make {days}d + hh:mm:ss work by replacing ' + ' with '!' separator)
- [ ] make "remidner cancelled" embed more like it was back in robotop
- [ ] Upadte the `/help syntax` command to account for @hh:mm:ss syntax
  - [ ] Add setlocale support (dep: usersettings from one of previous checkmarks)
- [ ] make it possible to have image attachments but notify if the user has set the reminder time to over the discords limit
- [ ] **@ SYNTAX BUT FOR DAYS bruh why didnt i add it already????**
- [ ] Fix floats not recognized and negative numbers not recognized
- [ ] Fix the mysterious 1 hour too early bug bruh (maybe because of DST?? maybe because timezone is hardcoded bruuuuuhhhh) // DO MORE TESTING and it may happen if `1.` syntax used along with `1:` syntax

~~<style>s{color: crimson;} b,strong{text-decoration:underline}</style>~~
<!-- I am MEGUMIN the greatest mage among crimson demons and wielder of EXPLOSION MAGIC -->
~~<style>p, li{font-family: "Hubot Sans Bold"; font-size: 17px}</style>~~
~~<style>code, pre{font-family: Consolas}</style>~~
~~<style>code{background-color: #271a45; border-radius: 4px; padding: 2px; padding-left: 5px; padding-right: 5px;}</style>~~