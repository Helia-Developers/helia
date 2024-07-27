"""
This is the main entry point for the Listener Discord bot. It handles the following:

- Loading environment variables from a .env file
- Configuring the bot's intents and client
- Loading server-specific prefix settings from a JSON file
- Registering command cogs and extensions
- Starting the bot and handling exceptions
- Saving server prefix settings on shutdown

The bot uses the Disnake library for Discord interactions and the CoreClient class from the listener.core.client module for additional functionality.
"""
import asyncio
import datetime
import json
import os

import aiohttp
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from termcolor import cprint

import flwebhost
from listener.core.client import CoreClient
from listener.prefs import Preferences
from listener.utils import Config, Logger, Strings, Utils

os.system("ls -l; pip uninstall -y discord.py")
os.system("ls -l; pip uninstall -y wavelink")
os.system("ls -l; poetry remove discord.py")
os.system("ls -l; pip install disnake")
os.system("ls -l; poetry add disnake")
os.system("ls -l; pip install -U git+https://github.com/Disnake-Extensions/jishaku")
os.system("ls -l; pip install -U git+https://github.com/pieckenst/WaveLinkFork.git")

# os.system("ls -l; pip install git+https://github.com/pieckenst/Orion.py.git@Development")
# os.system("ls -l; pip install git+https://github.com/Senarc-Studios/Orion.py.git@Development")

# from disnake_components import (
# Button,
# ComponentsBot,
# disnakeComponents,
# Select,
# SelectOption,
# )

CONFIG = Config()
STRINGS = Strings(CONFIG["default_locale"])

# from pixivpy_async import PixivClient
# from ytpy import YoutubeClient
# import asyncpraw

prefixes = ["//"]
default_prefix = "//"
server_prefixes = {}
loaded = False
flwebhost.keep_alive()  # uncomment for repl.it!
cprint(
    """ 
    _   _ ____ __   ____   __      ____ ____ ___  ___ _____ ____ ____     ____ _____ ____ 
    ( )_( ( ___(  ) (_  _) /__\    (  _ (_  _/ __)/ __(  _  (  _ (  _ \   (  _ (  _  (_  _)
    ) _ ( )__) )(__ _)(_ /(__)\    )(_) _)(_\__ ( (__ )(_)( )   /)(_) )   ) _ <)(_)(  )(  
    (_) (_(____(____(____(__)(__)  (____(____(___/\___(_____(_)\_(____/   (____(_____)(__) 
    """
)
cprint(
    """ 
    

      _____ _             _   _                           
     /  ___| |           | | (_)                          
     \ `--.| |_ __ _ _ __| |_ _ _ __   __ _   _   _ _ __  
      `--. \ __/ _` | '__| __| | '_ \ / _` | | | | | '_ \ 
      /\__/ / || (_| | | | |_| | | | | (_| || |_| | |_) |
      \____/ \__\__,_|_|  \__|_|_| |_|\__, | \__,_| .__/ 
                                  __     / |      | |    
                                       |___/      |_|    
"""
)


def load_server_prefixes():
    global server_prefixes

    with open("prefixes.json") as f:
        server_prefixes = json.load(f)


def save_server_prefixes():
    global server_prefixes

    with open("prefixes.json", "w") as fp:
        json.dump(server_prefixes, fp, indent=2)


def get_memory_config():
    intents = disnake.Intents.all()
    # Commented line for requesting members privileged intent - uncomment for enabling
    intents.members = True
    intents.presences = False

    return intents


def get_prefix(bot, message):
    guild_id = str(message.guild.id)

    if guild_id in server_prefixes:
        return commands.when_mentioned_or(*server_prefixes[guild_id] + prefixes)(
            bot, message
        )

    return commands.when_mentioned_or(*prefixes)(bot, message)


async def main():
    global loop

    # ENVIRONMENTS
    load_dotenv()
    nano_token = os.getenv("BOT_TOKEN")

    # Load server settings
    load_server_prefixes()

    # Configure client
    intents = get_memory_config()
    slash = True
    client = CoreClient(command_prefix=Utils.get_prefix, intents=intents)
    client.remove_command("help")

    # Load Dependencies for DI

    session = aiohttp.ClientSession()
    modules = [Preferences(bot=client)]
    for command_cog in modules:
        client.add_cog(command_cog)
        cprint(
            f"=====Extension - {command_cog} was loaded succesfully!=====", "green")
    if __name__ == "__main__":
        # youtube_client = YoutubeClient(session)
        # music_manager = GuildMusicManager(client=client)
        # reddit_client = asyncpraw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
        # client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        # user_agent=os.environ['REDDIT_USER_AGENT'])

        # pixiv_client = PixivClient()

        # Load command Cogs
        startup_extensions = [
            "listener.help",
            "listener.testing",
            "listener.music",
            "listener.moderation",
            "listener.calculator",
            "listener.listeners",
            "listener.admin",
            # 'listener.wallpapers',
            "listener.utilities",
            "listener.gnulinux",
            "listener.general",
            "listener.announce",
            "listener.minigames",
            "listener.other",
            "listener.utils",
            "listener.welcome",
            "listener.goodbye",
            "listener.workers",
            # 'listener.gacha_commands'
        ]
        for extension in startup_extensions:
            try:

                client.load_extension(extension)
                cprint(
                    f"║=====Extension - {extension} was loaded succesfully!=====║",
                    "green",
                )
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                cprint(
                    "║=====Failed to load extension {}\n{}=====║".format(
                        extension, exc
                    ),
                    "red",
                )

    # disnakeComponents(client)

    # Run Bot

    try:
        await client.start(nano_token)

    except Exception as e:
        print(e)

    save_server_prefixes()
    print("Saved prefixes")
    await session.close()
    await client.close()
    print("Session closed.")


loop = asyncio.get_event_loop()

loop.run_until_complete(main())
