# RoboBottom
A remake of **[RoboTop](https://robotop.xyz)**'s reminder system. RoboTop was originally made by **[Colon](https://gdcolon.com)** <img style="width: 15px; height: 15px;" src="https://cdn.discordapp.com/emojis/1132968267963715634.webp?size=64&name=fluff&quality=lossless"></img>. I only remade the reminders part of that bot because of its shutdown on August 12th 2023. RIP RoboTop, You will be missed!

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
(You might want to know this if you want to host the bot yourself)\
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
If i change my username for some reason here's my id `<@507642999992352779>`