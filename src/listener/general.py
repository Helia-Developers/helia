"""
A general-purpose cog that provides various utility commands for the bot, such as:

- `echo`: Sends a specified message as the bot.
- `embed`: Sends an embed with a specified name and content.
- `wiki`: Searches Wikipedia for a specified topic.
- `about`: Displays information about the bot and its author.
- `privacy`: Displays the bot's privacy policy.

This cog is designed to be a central hub for common bot functionality that doesn't fit into more specialized cogs.
"""

# -*- coding: utf-8 -*-
import datetime
import math
import os
import platform
import random
from typing import NoReturn

import disnake
import psutil
import wikipedia
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Commands, Config, Logger, Settings, Strings, Utils
from scripts import blacklist

CONFIG = Config()


class General(commands.Cog, name="General"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "General"
        self.process = psutil.Process(os.getpid())

    @commands.slash_command(name="echo", description="Echo msg")
    async def echo(self, inter: disnake.ApplicationCommandInteraction, content: str):
        if not content or len(content) > 200:
            await inter.response.send_message(
                "Invalid content. Please provide a non-empty message under 200 characters.",
                ephemeral=True,
            )
            return
        """
        A command to send a specified message as the bot.

        Parameters:
        -----------
        content: str
            The message to be echoed by the bot.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for item in blacklist.list:
                if content in item:
                    embed = disnake.Embed(
                        title=STRINGS["general"]["blacklistwarntitle"],
                        description=STRINGS["general"]["blacklistwarndesc"],
                        color=0xFF0000,
                    )
                    embed.set_footer(text=STRINGS["general"]["blacklistwarnfooter"])
                    return await inter.response.send_message(
                        embed=embed, ephemeral=True
                    )
            await inter.response.send_message(content)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="embed", description="Generate embed")
    async def embed(
        self, inter: disnake.ApplicationCommandInteraction, name: str, content: str
    ):
        """
        A command to send an embed with specified name and content as the bot.

        Parameters:
        -----------
        name: str
            The title of the embed.
        content: str
            The content of the embed.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for item in blacklist.list:
                if content in item:
                    embed = disnake.Embed(
                        title=STRINGS["general"]["blacklistwarntitle"],
                        description=STRINGS["general"]["blacklistwarndesc"],
                        color=0xFF0000,
                    )
                    embed.set_footer(text=STRINGS["general"]["blacklistwarnfooter"])
                    return await inter.response.send_message(
                        embed=embed, ephemeral=True
                    )
            creator = disnake.Embed(title=name, description=content)
            await inter.response.send_message(embed=creator)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="wiki", description="Search Wikipedia")
    @commands.is_nsfw()
    async def wiki(self, inter: disnake.ApplicationCommandInteraction, searcher: str):
        """
        A command to search Wikipedia for a specified topic.
        [REQUIRES NSFW CHANNEL! - Thank you top.gg for somehow finding nsfw there and as a result forcing this command to be restricted]

        Parameters:
        -----------
        searcher: str
            The topic to search for on Wikipedia.
        """
        try:
            wikipedia.set_lang("en")
            req = wikipedia.page(searcher)
            wikip = disnake.Embed(
                title=req.title,
                description="Wikipedia search results",
                url=req.url,
                color=0x269926,
            )
            wikip.set_thumbnail(url=req.images[0])
            await inter.response.send_message(embed=wikip)
        except wikipedia.exceptions.PageError:
            wikierror = disnake.Embed(
                title="Wikipedia Error",
                description="Page not found or some other error",
            )
            wikierror.add_field(
                name="If you are still having this error",
                value="Report the issue on github or ask in bot support server about it",
                inline=True,
            )
            wikierror.set_footer(text="Try again ")
            await inter.response.send_message(embed=wikierror)
        except disnake.ext.commands.errors.NSFWChannelRequired:
            nsfw_error = disnake.Embed(
                title="NSFW Channel Required",
                description="This command can only be used in NSFW channels.",
                color=0xFF0000,
            )
            await inter.response.send_message(embed=nsfw_error, ephemeral=True)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="about", description="about bot")
    async def about(self, inter: disnake.ApplicationCommandInteraction) -> NoReturn:
        """
        Shows a short description of the bot.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            path = "scripts/version.txt"
            with open(path, "r") as file:
                ver = file.readline()
            ramUsage = self.process.memory_full_info().rss / 1024**2
            pythonVersion = platform.python_version()
            dpyVersion = disnake.__version__
            servercount = len(self.bot.guilds)
            usercount = len(self.bot.users)
            delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = disnake.Embed(
                title=STRINGS["general"]["abouttitle"],
                description=STRINGS["general"]["aboutdesc"],
                color=0xFF6900,
            )

            embed.add_field(
                name=STRINGS["general"]["aboutver"],
                value=f" Version: {ver}\nPython Version:{pythonVersion}\nLibrary: disnake.py\ndisnake.Py Version: {dpyVersion} ",
                inline=False,
            )
            embed.add_field(
                name="Other Information",
                value=f" Count: {servercount}\nUser Count: {usercount}\nRAM Usage:{ramUsage:.2f} MB\nDays: {days}d\nHours: {hours}h\nMinutes: {minutes}m\nSeconds: {seconds}s\nCommand Count: {len(self.bot.commands)}",
                inline=True,
            )
            embed.add_field(
                name=STRINGS["general"]["aboutauthor"],
                value=STRINGS["general"]["aboutauthortext"],
                inline=True,
            )

            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await inter.response.send_message(embed=embed)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="privacy", description="privacy policy")
    async def privacy(self, inter: disnake.ApplicationCommandInteraction):
        """
        Shows the privacy policy of the bot.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            embed = disnake.Embed(
                title=STRINGS["privacy"]["privtitle"],
                description=STRINGS["privacy"]["privdesc"],
                color=0xFF8040,
            )
            embed.add_field(
                name=STRINGS["privacy"]["terminologytitle"],
                value=STRINGS["privacy"]["terminologydesc"],
                inline=True,
            )
            embed.add_field(
                name=STRINGS["privacy"]["datacollecttitle"],
                value=STRINGS["privacy"]["datacollectdesc"],
                inline=True,
            )
            embed.add_field(
                name=STRINGS["privacy"]["dctitlecont"],
                value=STRINGS["privacy"]["datacollectcont"],
                inline=True,
            )
            embed.add_field(
                name=STRINGS["privacy"]["loggingtitle"],
                value=STRINGS["privacy"]["loggingdesc"],
                inline=True,
            )
            embed.add_field(
                name=STRINGS["privacy"]["securitytitle"],
                value=STRINGS["privacy"]["securitydesc"],
                inline=True,
            )
            embed.add_field(
                name=STRINGS["privacy"]["datadeletepoltitle"],
                value=STRINGS["privacy"]["datadeletepoldesc"],
                inline=True,
            )
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await inter.response.send_message(embed=embed)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(General(bot))
    Logger.cog_loaded(bot.get_cog("General").name)
