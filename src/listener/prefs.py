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

    @commands.slash_command(name="prefix", description="Sets a custom prefix")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(
        self, inter: disnake.ApplicationCommandInteraction, prefix: str
    ) -> NoReturn:
        """Sets a custom prefix.

        Parameters:
        -----------
        prefix: The new prefix to set
        """
        s = await Settings(inter.guild.id)
        await s.set_field("prefix", prefix)
        embed = disnake.Embed(title=f"Prefix has been set to {prefix}", color=0x0C0C0C)
        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="locale", description="Sets bot language")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def locale(
        self, inter: disnake.ApplicationCommandInteraction, locale: str
    ) -> NoReturn:
        """Sets bot language. If not found, it throws an error.

        Parameters:
        -----------
        locale: The new locale to set
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        locales = Utils.get_locales_list()

        for _locale in locales:
            if _locale == locale:
                await s.set_field("locale", locale)
                embed = disnake.Embed(title="Locale successfully set!", color=0x0C0C0C)
                await inter.response.send_message(embed=embed, ephemeral=True)
                return

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
        print(f"Wrong localization given on {inter.guild}")
        await inter.response.send_message(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Preferences(bot))
    Logger.cog_loaded(bot.get_cog("Preferences").name)
