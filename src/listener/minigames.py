import asyncio
import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings
from scripts import games

CONFIG = Config()


class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        slash_interaction=False, message_command=True, description="Random cube"
    )
    async def kubik(self, ctx: Context):  # кубик рандом
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        kuboid = random.choice(games.kubik)
        embedkub = disnake.Embed(
            title=STRINGS["other"]["rollcubetitle"], color=0x00FF00
        )
        embedkub.add_field(name=STRINGS["other"]["rolled"], value=kuboid, inline=False)
        await ctx.send(embed=embedkub)

    @commands.command(
        slash_interaction=False, message_command=True, description="Coin throw"
    )
    async def monetka(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        mon = random.choice(games.monet)
        embedmonet = disnake.Embed(
            title=STRINGS["other"]["cointosstitle"], color=0x00FF00
        )
        embedmonet.add_field(name=STRINGS["other"]["rolled"], value=mon, inline=False)
        await ctx.send(embed=embedmonet)

    @commands.command(
        slash_interaction=False, message_command=True, description="Casino"
    )
    async def casino(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        kasino1 = random.choice(games.casin_obj1)
        kasino2 = random.choice(games.casin_obj2)
        kasino3 = random.choice(games.casin_obj3)
        embedkas = disnake.Embed(title=STRINGS["other"]["casinotitle"], color=0x00FF00)
        embedkas.add_field(name=STRINGS["other"]["rolled"], value=kasino1, inline=True)
        embedkas.add_field(name=STRINGS["other"]["rolled"], value=kasino2, inline=True)
        embedkas.add_field(name=STRINGS["other"]["rolled"], value=kasino3, inline=True)
        await ctx.send(embed=embedkas)


def setup(client):
    client.add_cog(minigames(client))
