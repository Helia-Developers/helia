"""
This class provides commands for managing user preferences, such as setting a custom prefix and locale (language) for the bot. The `prefix` command allows administrators to set a custom prefix for the bot, which will be used to trigger commands. The `locale` command allows administrators to set the bot's language, which will affect the strings and messages displayed by the bot.

The `Preferences` class inherits from `commands.Cog`, which is a way to organize related commands in a Discord bot. The class has two main commands:

1. `prefix`: Sets a custom prefix for the bot. This command is only available to users with the "administrator" permission.
2. `locale`: Sets the bot's language. This command is only available to users with the "administrator" permission.

Both commands use the `Settings` class to store and retrieve the user's preferences, and they display the updated settings to the user using a Discord embed.
"""

# -*- coding: utf-8 -*-
from typing import NoReturn

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Preferences(commands.Cog, name="Preferences"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "Preferences"
        # self.server_prefixes = server_prefixes

    @commands.command(slash_command=True, message_command=True,aliases=["setprefix"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx: Context, prefix: str) -> NoReturn:
        """Sets a custom prefix.

        Attributes:
        -----------
        - `prefix` - new prefix

        """
        s = await Settings(ctx.guild.id)
        await s.set_field("prefix", prefix)
        embederx=disnake.Embed(title=f"Prefix has been set to {prefix}", color=0x0c0c0c)
        await ctx.send(embed=embederx,ephemeral=True)

        #await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True, message_command=True,aliases=["lang", "setlang", "language"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def locale(self, ctx: Context, locale: str) -> NoReturn:
        """Sets bot language. If not found, it throws an error.

        Attributes:
        -----------
        - `locale` - new locale

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        locales = Utils.get_locales_list()

        for _locale in locales:
            if _locale == locale:
                await s.set_field("locale", locale)
                embederx=disnake.Embed(title=f"Locale succesfully set!", color=0x0c0c0c)
                await ctx.send(embed=embederx,ephemeral=True)

                #await ctx.message.add_reaction(CONFIG["yes_emoji"])
                return

        # FIXME
        embed = disnake.Embed(
            title=STRINGS["error"]["on_error_title"],
            description=STRINGS["error"]["localeerrortext"],
            color=0xFF0000,
        )
        embed.add_field(
            name=STRINGS["error"]["generictracebackthing"],
            value=STRINGS["error"]["localerrrorstring"],
            inline=False,
        )
        print(f"Wrong localization given on {ctx.message.guild}")
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Preferences(bot))
    Logger.cog_loaded(bot.get_cog("Preferences").name)
