# -*- coding: utf-8 -*-
import random
from typing import NoReturn

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings, Utils
from scripts import desAnime, desNature, desStarwars

CONFIG = Config()


class Other(commands.Cog, name="Other"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Other"

    @commands.command(slash_interaction=True, message_command=True)
    async def ping(self, ctx: Context) -> NoReturn:
        """Shows host latency."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        latency = "%.0fms" % (self.bot.latency * 100)
        embed = disnake.Embed(
            title="{} Latency".format(self.bot.name),
            description=f":hourglass_flowing_sand: {latency} ",
            color=0xFF8000,
        )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def wallpaper(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        wallinfo = disnake.Embed(
            title=STRINGS["wallpaper"]["wallpaperembedtitle"],
            description=STRINGS["wallpaper"]["wallpaperdesc"],
            color=0x00FF00,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusageanimetitle"],
            value="``wallpaper anime``",
            inline=True,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusagenaturetitle"],
            value="``wallpaper nature``",
            inline=True,
        )
        wallinfo.add_field(
            name=STRINGS["wallpaper"]["wallpaperusagestarwarstitle"],
            value="``wallpaper starwars``",
            inline=True,
        )
        await ctx.send(embed=wallinfo)

    @wallpaper.command()
    async def anime(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embedanime = disnake.Embed(
            title=STRINGS["wallpaper"]["wallpaperanimetitle"],
            color=0x00FF00,
        )
        embedanime.set_footer(text=STRINGS["wallpaper"]["wallpaperanimefooter"])
        await ctx.send(embed=embedanime)

    @wallpaper.command()
    async def nature(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        imgnat = random.choice(desNature.images)
        embednat = disnake.Embed(
            title=STRINGS["wallpaper"]["wallpapernaturetitle"],
            color=0x00FF00,
            url=imgnat,
        )
        embednat.set_image(url=imgnat)
        await ctx.send(embed=embednat)

    @wallpaper.command()
    async def starwars(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        imgstarwars = random.choice(desStarwars.images)
        embedstarwars = disnake.Embed(
            title=STRINGS["wallpaper"]["wallpaperstarwarstitle"],
            color=0x00FF00,
            url=imgstarwars,
        )
        embedstarwars.set_image(url=imgstarwars)
        await ctx.send(embed=embedstarwars)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog("Other").name)
