# -*- coding: utf-8 -*-
from typing import NoReturn

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Prefs(commands.Cog, name="Prefs"):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "Prefs"
        # self.server_prefixes = server_prefixes

    @commands.command(aliases=["setprefix"])
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

        await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(aliases=["lang", "setlang", "language"])
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

                await ctx.message.add_reaction(CONFIG["yes_emoji"])
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
    bot.add_cog(Prefs(bot))
    Logger.cog_loaded(bot.get_cog("Prefs").name)
