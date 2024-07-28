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

    @commands.slash_command(name="ping", description="Check ping")
    async def ping(self,
                   inter: disnake.ApplicationCommandInteraction) -> NoReturn:
        """
        Shows the bot's latency.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        NoReturn
        """
        try:
            EMBED_COLOR=0xFF8000
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            latency = "%.0fms" % (self.bot.latency * 100)
            embed = disnake.Embed (
                title=f"{self.bot.name} Latency",
                description=f":hourglass_flowing_sand: {latency} ",
                # Define the color constant at the module level
                color=EMBED_COLOR,
            )
                

                # Use the constant in your embed creation
            embed=disnake.Embed(
                    title=STRINGS["moderation"]["setstatustext"],
                    description=STRINGS["moderation"]["setstatusdesc"],
                    color=EMBED_COLOR,
                )
            
            await inter.response.send_message(embed=embed)
        except Exception as e:
            Logger.error(f"Error in ping command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @commands.slash_command(name="wallpaper", description="Get wallpaper")
    async def wallpaper(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays wallpaper information and available options.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        NoReturn
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            wallinfo = disnake.Embed(
                title=STRINGS["wallpaper"]["wallpaperembedtitle"],
                description=STRINGS["wallpaper"]["wallpaperdesc"],
                color=0x00FF00,
            )
            wallinfo.add_field(
                name=STRINGS["wallpaper"]["wallpaperusageanimetitle"],
                value="``/wallpaper anime``",
                inline=True,
            )
            wallinfo.add_field(
                name=STRINGS["wallpaper"]["wallpaperusagenaturetitle"],
                value="``/wallpaper nature``",
                inline=True,
            )
            wallinfo.add_field(
                name=STRINGS["wallpaper"]["wallpaperusagestarwarstitle"],
                value="``/wallpaper starwars``",
                inline=True,
            )
            await inter.response.send_message(embed=wallinfo)
        except Exception as e:
            Logger.error(f"Error in wallpaper command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @wallpaper.sub_command(name="anime", description="Get an anime wallpaper")
    async def anime(self, inter: disnake.ApplicationCommandInteraction):
        """
        Sends an anime wallpaper.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        NoReturn
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            embedanime = disnake.Embed(
                title=STRINGS["wallpaper"]["wallpaperanimetitle"],
                color=0x00FF00,
            )
            embedanime.set_footer(
                text=STRINGS["wallpaper"]["wallpaperanimefooter"])
            await inter.response.send_message(embed=embedanime)
        except Exception as e:
            Logger.error(f"Error in anime wallpaper command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @wallpaper.sub_command(name="nature", description="Get a nature wallpaper")
    async def nature(self, inter: disnake.ApplicationCommandInteraction):
        """
        Sends a nature wallpaper.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        NoReturn
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            imgnat = random.choice(desNature.images)
            embednat = disnake.Embed(
                title=STRINGS["wallpaper"]["wallpapernaturetitle"],
                color=0x00FF00,
                url=imgnat,
            )
            embednat.set_image(url=imgnat)
            await inter.response.send_message(embed=embednat)
        except Exception as e:
            Logger.error(f"Error in nature wallpaper command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)

    @wallpaper.sub_command(name="starwars",
                           description="Get a Star Wars wallpaper")
    async def starwars(self, inter: disnake.ApplicationCommandInteraction):
        """
        Sends a Star Wars wallpaper.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Returns:
        --------
        NoReturn
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            imgstarwars = random.choice(desStarwars.images)
            embedstarwars = disnake.Embed(
                title=STRINGS["wallpaper"]["wallpaperstarwarstitle"],
                color=0x00FF00,
                url=imgstarwars,
            )
            embedstarwars.set_image(url=imgstarwars)
            await inter.response.send_message(embed=embedstarwars)
        except Exception as e:
            Logger.error(f"Error in Star Wars wallpaper command: {str(e)}")
            await inter.response.send_message(
                "An error occurred while processing the command.",
                ephemeral=True)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Other(bot))
    Logger.cog_loaded(bot.get_cog("Other").name)
