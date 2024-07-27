"""
Provides utility functions and classes for the Discord bot.

The `Config` class loads the bot's configuration from a JSON file.

The `Commands` class provides a way to load command translations from locale-specific JSON files.

The `Settings` class manages the bot's settings, which are stored in a JSON file. It provides methods to create, retrieve, and update settings fields.

The `Strings` class provides a way to load locale-specific strings from JSON files.

The `Logger` class provides logging functions to print messages with different levels of severity.

The `Utils` class is a Discord command extension that provides utility functions, such as creating embeds with different colors.
"""

# -*- coding: utf-8 -*-
import datetime
import json
import os
from os.path import abspath, dirname
from typing import Any, AnyStr, Dict, List, NoReturn

from aiofile import async_open
from asyncinit import asyncinit
from disnake import Embed, Message
from disnake.ext import commands
from disnake.ext.commands import Bot
from termcolor import cprint


class Config:
    cfg = None

    def __new__(self) -> Any:
        with open(dirname(abspath(__file__)) + "/../data/config.json",
                  "r") as f:
            return json.load(f)


CONFIG = Config()


class Commands:

    def __listdirs(path: AnyStr) -> List[str]:
        return [
            d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))
        ]

    def __new__(self, locale: AnyStr = "") -> Dict:
        dirs = self.__listdirs(
            dirname(abspath(__file__)) + "/../data/locales/")

        if locale in dirs or locale != "":
            with open(
                    dirname(abspath(__file__)) +
                    f"/../data/locales/{locale}/commands.json",
                    "r",
            ) as f:
                return json.load(f)
        else:
            CONFIG = Config()
            with open(
                    dirname(abspath(__file__)) +
                    f'/../data/locales/{CONFIG["default_locale"]}/commands.json',
                    "r",
            ) as f:
                return json.load(f)


@asyncinit
class Settings:
    guild_id: int = 0
    settings: Dict = None

    async def __init__(self, _guild_id: int) -> None:
        self.guild_id = _guild_id

        async with async_open(
                dirname(abspath(__file__)) + "/../data/settings.json",
                "r") as f:
            self.settings = json.loads(await f.read())

    async def __save(self) -> NoReturn:
        async with async_open(
                dirname(abspath(__file__)) + "/../data/settings.json",
                "w") as f:
            await f.write(json.dumps(self.settings, indent=4))

    async def __create_guild_object(self) -> NoReturn:
        self.settings[str(str(self.guild_id))] = {}
        await self.__save()

    async def create_empty_field(self, field: AnyStr) -> NoReturn:
        try:
            self.settings[str(self.guild_id)][field] = None
            await self.__save()
        except:
            await self.__create_guild_object()
            self.settings[str(self.guild_id)][field] = None
            await self.__save()

    async def get_field(self, field: AnyStr, default_value: Any = None) -> Any:
        try:
            val = self.settings[str(self.guild_id)][field]
        except:
            await self.create_empty_field(field)
            val = self.settings[str(self.guild_id)][field]

        if val is not None or default_value is None:
            return self.settings[str(self.guild_id)][field]

        await self.set_field(field, default_value)
        return default_value

    async def set_field(self, field: AnyStr, value) -> NoReturn:
        try:
            self.settings[str(self.guild_id)][field] = value
            await self.__save()
        except:
            await self.create_empty_field(field)
            self.settings[str(self.guild_id)][field] = value
            await self.__save()


class Strings:

    def __listdirs(path: AnyStr) -> List[str]:
        return [
            d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))
        ]

    def __new__(self, locale: AnyStr = "") -> Dict:
        dirs = self.__listdirs(
            dirname(abspath(__file__)) + "/../data/locales/")

        if locale in dirs or locale != "":
            with open(
                    dirname(abspath(__file__)) +
                    f"/../data/locales/{locale}/strings.json",
                    "r",
            ) as f:
                return json.load(f)
        else:
            CONFIG = Config()
            with open(
                    dirname(abspath(__file__)) +
                    f'/../data/locales/{CONFIG["default_locale"]}/strings.json',
                    "r",
            ) as f:
                return json.load(f)


"""
    Provides logging utilities for the bot.
    
    The `Logger` class provides several static methods for logging different types of messages, such as informational, warning, and error messages. These methods use the `Strings` class to retrieve localized strings for the log messages, and format the messages with the current timestamp.
    
    The `done` method logs an informational message with a green color.
    The `warn` method logs a warning message with a red color.
    The `cog_loaded` method logs a message indicating that a cog has been loaded.
    The `command_used` method logs a message indicating that a command has been used, with the command name, the tag, and the guild name.
    """


class Logger:

    def done(msg: AnyStr) -> NoReturn:
        STRINGS = Strings(CONFIG["default_locale"])
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        cprint(STRINGS["bot_log"]["info"].format(time, msg), "green")

    def warn(msg: AnyStr) -> NoReturn:
        STRINGS = Strings(CONFIG["default_locale"])
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        cprint(STRINGS["bot_log"]["warn"].format(time, msg), "red")  #

    # some wrappers:

    def cog_loaded(cog: AnyStr) -> NoReturn:
        STRINGS = Strings(CONFIG["default_locale"])
        now = datetime.datetime.now()
        time = now.strftime("%HH:%MM:%SS")
        cprint(
            """║============================================================║"""
        )
        # cprint(
        # STRINGS["bot_log"]["info"].format(time, STRINGS["bot_log"]["cog_loaded"].format(cog)),
        # "green",
        # )
        cprint(
            """║============================================================║"""
        )

    def command_used(tag: AnyStr, command: AnyStr, guild: AnyStr) -> NoReturn:
        STRINGS = Strings(CONFIG["default_locale"])
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        cprint(
            STRINGS["bot_log"]["log_cmd"].format(time, tag, command, guild),
            "green",
            attrs=["dark"],
        )


class Utils(commands.Cog, name="Utils"):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Utils"

    def done_embed(msg: Message) -> Embed:
        return Embed(color=0x00FF47, description=msg)

    def warn_embed(msg: Message) -> Embed:
        return Embed(color=0xFFD600, description=msg)

    def error_embed(msg: Message) -> Embed:
        return Embed(color=0xED4242, description=msg)

    async def get_prefix(bot: Bot, msg: Message) -> List[str]:
        s = await Settings(msg.guild.id)
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        return [
            bot.user.mention + " ", f"<@!{bot.user.id}> ", prefix, prefix + " "
        ]

    def get_locales_list():

        def __listdirs(path: AnyStr) -> List[str]:
            return [
                d for d in os.listdir(path)
                if os.path.isdir(os.path.join(path, d))
            ]

        return __listdirs(dirname(abspath(__file__)) + "/../data/locales/")


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Utils(bot))
    Logger.cog_loaded(bot.get_cog("Utils").name)
