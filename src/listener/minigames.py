"""
A cog that provides various mini-game commands for a Discord bot.

This cog includes the following commands:
- `kubik`: Rolls a random cube and displays the result.
- `monetka`: Flips a coin and displays the result.
- `casino`: Generates a random casino-style result with three random elements.

These commands are available as slash commands.
"""

import asyncio
import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings
from scripts import games

CONFIG = Config()


class Minigames(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kubik", description="Roll a random cube")
    async def kubik(self, inter: disnake.ApplicationCommandInteraction):
        """
        Roll a random cube and display the result.

        This command generates a random cube face and sends an embed message with the result.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        None
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            kuboid = random.choice(games.kubik)
            embedkub = disnake.Embed(title=STRINGS["other"]["rollcubetitle"],
                                     color=0x00FF00)
            embedkub.add_field(name=STRINGS["other"]["rolled"],
                               value=kuboid,
                               inline=False)
            await inter.response.send_message(embed=embedkub)
        except Exception as e:
            Logger.error(f"Error in kubik command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @commands.slash_command(name="monetka", description="Flip a coin")
    async def monetka(self, inter: disnake.ApplicationCommandInteraction):
        """
        Flip a coin and display the result.

        This command simulates a coin flip and sends an embed message with the result.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        None
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            mon = random.choice(games.monet)
            embedmonet = disnake.Embed(title=STRINGS["other"]["cointosstitle"],
                                       color=0x00FF00)
            embedmonet.add_field(name=STRINGS["other"]["rolled"],
                                 value=mon,
                                 inline=False)
            await inter.response.send_message(embed=embedmonet)
        except Exception as e:
            Logger.error(f"Error in monetka command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @commands.slash_command(name="casino", description="Play a casino game")
    async def casino(self, inter: disnake.ApplicationCommandInteraction):
        """
        Generate a random casino-style result with three random elements.

        This command simulates a casino game by generating three random elements and
        sending an embed message with the results.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        None
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            kasino1 = random.choice(games.casin_obj1)
            kasino2 = random.choice(games.casin_obj2)
            kasino3 = random.choice(games.casin_obj3)
            embedkas = disnake.Embed(title=STRINGS["other"]["casinotitle"],
                                     color=0x00FF00)
            embedkas.add_field(name=STRINGS["other"]["rolled"],
                               value=kasino1,
                               inline=True)
            embedkas.add_field(name=STRINGS["other"]["rolled"],
                               value=kasino2,
                               inline=True)
            embedkas.add_field(name=STRINGS["other"]["rolled"],
                               value=kasino3,
                               inline=True)
            await inter.response.send_message(embed=embedkas)
        except Exception as e:
            Logger.error(f"Error in casino command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)


def setup(client):
    client.add_cog(Minigames(client))
