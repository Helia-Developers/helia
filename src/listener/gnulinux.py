"""
A Cog that provides slash commands for displaying information about various GNU/Linux distributions.

This Cog includes the following commands:
- `/arch`: Displays information about Arch Linux.
- `/ubuntu`: Displays information about Ubuntu Linux.
- `/debian`: Displays information about Debian Linux.
- `/deepin`: Displays information about Deepin Linux.
- `/manjaro`: Displays information about Manjaro Linux.
- `/mint`: Displays information about Linux Mint.

The information displayed for each distribution includes a description, a thumbnail image, and a link to the distribution's website.
"""

# LOCALIZATION SUPPORT NEEDS IMPLEMENTING
import asyncio

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class GNULinux(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="arch",
        description="Display information about Arch Linux",
    )
    async def arch(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Arch Linux.

        This command sends an embed containing a description, thumbnail, and link for Arch Linux.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            archl = disnake.Embed(
                title="Arch Linux",
                url="https://www.archlinux.org/download/",
                description=STRINGS["gnulinuxx"]["archdesc"],
                color=0x1793D1,
            )
            archl.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/1280px-Archlinux-vert-dark.svg.png"
            )
            await inter.response.send_message(embed=archl)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)

    @commands.slash_command(
        name="ubuntu",
        description="Display information about Ubuntu Linux",
    )
    async def ubuntu(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Ubuntu Linux.

        This command sends an embed containing a description, thumbnail, and link for Ubuntu Linux.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            ubuntu1 = disnake.Embed(
                title="Ubuntu",
                url="https://ubuntu.com/",
                description=STRINGS["gnulinuxx"]["ubuntudesc"],
                color=0xDE4714,
            )
            ubuntu1.set_thumbnail(url="https://i.imgur.com/TfVgK1v.png")
            await inter.response.send_message(embed=ubuntu1)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)

    @commands.slash_command(
        name="debian",
        description="Display information about Debian Linux",
    )
    async def debian(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Debian Linux.

        This command sends an embed containing a description, thumbnail, and link for Debian Linux.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            debian1 = disnake.Embed(
                title="Debian",
                url="https://www.debian.org/",
                description=STRINGS["gnulinuxx"]["debiandesc"],
                color=0xD80150,
            )
            debian1.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/800px-Debian-OpenLogo.svg.png"
            )
            await inter.response.send_message(embed=debian1)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)

    @commands.slash_command(
        name="deepin",
        description="Display information about Deepin Linux",
    )
    async def deepin(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Deepin Linux.

        This command sends an embed containing a description, thumbnail, and link for Deepin Linux.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            deepin1 = disnake.Embed(
                title="Deepin",
                url="https://www.deepin.org",
                description=STRINGS["gnulinuxx"]["deeepindesc"],
                color=0x1793D1,
            )
            deepin1.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Deepin_logo.svg/600px-Deepin_logo.svg.png"
            )
            await inter.response.send_message(embed=deepin1)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)

    @commands.slash_command(
        name="manjaro",
        description="Display information about Manjaro Linux",
    )
    async def manjaro(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Manjaro Linux.

        This command sends an embed containing a description, thumbnail, and link for Manjaro Linux.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            manjaro1 = disnake.Embed(
                title="Manjaro",
                url="https://manjaro.org/",
                description=STRINGS["gnulinuxx"]["manjarodesc"],
                color=0x35BF5C,
            )
            manjaro1.set_thumbnail(
                url="https://fost.ws/uploads/posts/2019-05/1557568788_manjaro-logo.png"
            )
            await inter.response.send_message(embed=manjaro1)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)

    @commands.slash_command(
        name="mint",
        description="Display information about Linux Mint",
    )
    async def mint(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays information about Linux Mint.

        This command sends an embed containing a description, thumbnail, and link for Linux Mint.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object representing the command invocation.

        Raises:
        -------
        disnake.HTTPException
            If there was an error sending the message.
        disnake.Forbidden
            If the bot doesn't have permission to send messages in the channel.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            mint1 = disnake.Embed(
                title="Linux Mint",
                url="https://linuxmint.com/",
                description=STRINGS["gnulinuxx"]["mintdesc"],
                color=0xB1EA77,
            )
            mint1.set_thumbnail(url="https://i.imgur.com/cyRjcbp.png")
            await inter.response.send_message(embed=mint1)
        except (disnake.HTTPException, disnake.Forbidden) as e:
            await inter.response.send_message(f"An error occurred: {str(e)}",
                                              ephemeral=True)


def setup(bot):
    bot.add_cog(GNULinux(bot))
