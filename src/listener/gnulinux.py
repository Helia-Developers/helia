"""
A Cog that provides commands for displaying information about various GNU/Linux distributions.

This Cog includes the following commands:
- `arch`: Displays information about Arch Linux.
- `ubuntu`: Displays information about Ubuntu Linux.
- `debian`: Displays information about Debian Linux.
- `deepin`: Displays information about Deepin Linux.
- `manjaro`: Displays information about Manjaro Linux.
- `mint`: Displays information about Linux Mint.

The information displayed for each distribution includes a description, a thumbnail image, and a link to the distribution's website.
"""
# LOCALIZATION SUPPORT NEEDS IMPLEMENTING
import asyncio

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class gnulinux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # GNU/Linux Distr Wiki
    @commands.command(
        slash_command=False,
        message_command=True,
        description="Arch Linux Description",
    )
    async def arch(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        archl = disnake.Embed(
            title="Arch Linux",
            url="https://www.archlinux.org/download/",
            description=STRINGS["gnulinuxx"]["archdesc"],
            color=0x1793D1,
        )
        archl.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/1280px-Archlinux-vert-dark.svg.png"
        )
        await ctx.send(embed=archl)

    @commands.command(
        slash_command=False,
        message_command=True,
        description="Ubuntu linux description",
    )
    async def ubuntu(self, ctx: Context):  # Ubuntu
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        ubuntu1 = disnake.Embed(
            title="Ubuntu",
            url="https://ubuntu.com/",
            description=STRINGS["gnulinuxx"]["ubuntudesc"],
            color=0xDE4714,
        )
        ubuntu1.set_thumbnail(url="https://i.imgur.com/TfVgK1v.png")
        await ctx.send(embed=ubuntu1)

    @commands.command(
        slash_command=False,
        message_command=True,
        description="Debian Linux Description",
    )
    async def debian(self, ctx: Context):  # Debian
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        debian1 = disnake.Embed(
            title="Debian",
            url="https://www.debian.org/",
            description=STRINGS["gnulinuxx"]["debiandesc"],
            color=0xD80150,
        )
        debian1.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/800px-Debian-OpenLogo.svg.png"
        )
        await ctx.send(embed=debian1)

    @commands.command(
        slash_command=False,
        message_command=True,
        description="Deepin linux description",
    )
    async def deepin(self, ctx: Context):  # Deepin
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        deepin1 = disnake.Embed(
            title="Deepin",
            url="https://www.deepin.org",
            description=STRINGS["gnulinuxx"]["deeepindesc"],
            color=0x1793D1,
        )
        deepin1.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Deepin_logo.svg/600px-Deepin_logo.svg.png"
        )
        await ctx.send(embed=deepin1)

    @commands.command(
        slash_command=False,
        message_command=True,
        description="Manjaro linux description",
    )
    async def manjaro(self, ctx: Context):  # Manjaro
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        manjaro1 = disnake.Embed(
            title="Manjaro",
            url="https://manjaro.org/",
            description=STRINGS["gnulinuxx"]["manjarodesc"],
            color=0x35BF5C,
        )
        manjaro1.set_thumbnail(
            url="https://fost.ws/uploads/posts/2019-05/1557568788_manjaro-logo.png"
        )
        await ctx.send(embed=manjaro1)

    @commands.command(
        slash_command=False,
        message_command=True,
        description="Linux Mint description",
    )
    async def mint(self, ctx: Context):  # Mint
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        channel = ctx.message.channel
        mint1 = disnake.Embed(
            title="Linux Mint",
            url="https://linuxmint.com/",
            description=STRINGS["gnulinuxx"]["mintdesc"],
            color=0xB1EA77,
        )
        mint1.set_thumbnail(url="https://i.imgur.com/cyRjcbp.png")
        await ctx.send(embed=mint1)


def setup(bot):
    bot.add_cog(gnulinux(bot))
