# -*- coding: utf-8 -*-
import datetime
import math
import os
import platform
import random
from typing import NoReturn

import discord
import psutil
import wikipedia
from discord.ext import commands
from discord.ext.commands import Bot, Context

from listener.utils import Commands, Config, Logger, Settings, Strings, Utils
from scripts import blacklist

CONFIG = Config()


class General(commands.Cog, name="General"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "General"
        self.process = psutil.Process(os.getpid())

    # @commands.command()
    # @commands.guild_only()
    # async def fuglyhelp(self, ctx: Context, command: str = None) -> NoReturn:
    # """Shows help for a specific command, or displays a complete list of commands.
    # Attributes:
    # -----------
    # - `command` - the command to display help for.
    #    If `command` is empty, displays a complete list of commands.
    #    If the command does not exist, writes that the command was not found.
    # """
    # s = await Settings(ctx.guild.id)
    # lang = await s.get_field('locale', CONFIG['default_locale'])
    # prefix = await s.get_field('prefix', CONFIG['default_prefix'])
    # STRINGS = Strings(lang)
    # COMMANDS = Commands(lang)

    # if command == None:
    # embed = discord.Embed(
    # title=STRINGS['general']['commands_list'], description=STRINGS['general']['help_list_description'].format(prefix), color=0xef940b)
    # embed.set_thumbnail(
    # url=self.bot.user.avatar.url)

    # for i in COMMANDS:
    # title = COMMANDS[i]['title']

    # description = ', '.join(
    # [f'`{j}`' for j in COMMANDS[i]['commands']])

    # if self.bot.get_cog(i) != None:
    # embed.add_field(
    # name=title, value=description, inline=False)

    # await ctx.send(embed=embed)

    # elif command != '':
    # for i in COMMANDS:
    # for j in COMMANDS[i]['commands']:
    # if command == j:
    # embed = discord.Embed(
    # title=STRINGS['general']['help'].format(f'`{prefix}{j}`'), color=0xef940b)

    # embed.set_thumbnail(
    # url=self.bot.user.avatar.url)

    # embed.add_field(
    # name=STRINGS['general']['description'], value=COMMANDS[i]['commands'][j]['description'], inline=False)

    # embed.add_field(
    # name=STRINGS['general']['usage'], value=COMMANDS[i]['commands'][j]['usage'].format(prefix), inline=False)

    # if len(COMMANDS[i]['commands'][j]['aliases']) > 0:
    # aliases = ', '.join(
    # [f'`{alias}`' for alias in COMMANDS[i]['commands'][j]['aliases']])
    # embed.add_field(
    # name=STRINGS['general']['aliases'], value=aliases, inline=False)

    # await ctx.send(embed=embed)
    # return
    # else:
    # await ctx.send(embed=Utils.error_embed(STRINGS['error']['command_not_found']))

    @commands.command(
        slash_interaction=True, message_command=True, description="Echo Commands"
    )
    async def echo(self, ctx: Context, *, content):
        """


        A command to send a specified message as bot

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        STRINGS = Strings(lang)
        for item in blacklist.list:
            if content in item:
                await ctx.message.delete()
                embed = discord.Embed(
                    title=STRINGS["general"]["blacklistwarntitle"],
                    description=STRINGS["general"]["blacklistwarndesc"],
                    color=0xFF0000,
                )
                embed.set_footer(text=STRINGS["general"]["blacklistwarnfooter"])
                return await ctx.send(embed=embed)
        else:
            return await ctx.send(content)

    @commands.command(
        slash_interaction=True, message_command=True, description="Generate Embed"
    )
    async def embed(self, ctx: Context, name, *, content):
        """


        A command to send a embed with specified name and content as bot

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        STRINGS = Strings(lang)
        for item in blacklist.list:
            if content in item:
                await ctx.message.delete()
                embed = discord.Embed(
                    title=STRINGS["general"]["blacklistwarntitle"],
                    description=STRINGS["general"]["blacklistwarndesc"],
                    color=0xFF0000,
                )
                embed.set_footer(text=STRINGS["general"]["blacklistwarnfooter"])
                return await ctx.send(embed=embed)
        else:
            creator = discord.Embed(title=name, description=content)
            await ctx.send(embed=creator)

    @commands.command(
        slash_interaction=True, message_command=True, description="Search Wikipedia"
    )
    @commands.is_nsfw()
    async def wiki(self, ctx: Context, *, searcher=None):
        """


        A command to search wikipedia for a specified topic
        [REQUIRES NSFW CHANNEL! - Thank you top.gg for somehow fucking finding nsfw there and as a result forcing this command to be restricted]

        """
        try:
            wikipedia.set_lang("en")
            req = wikipedia.page(searcher)
            wikip = discord.Embed(
                title=req.title,
                description="Wikipedia search results",
                url=req.url,
                color=0x269926,
            )
            wikip.set_thumbnail(url=req.images[0])
            await ctx.send(embed=wikip)
        except wikipedia.exceptions.PageError:
            wikierror = discord.Embed(
                title="Wikipedia Error",
                description="Page not found or some other error",
            )
            wikierror.add_field(
                name="If you are still having this error",
                value="Report the issue on github or ask in bot support server about it",
                inline=True,
            )
            wikierror.set_footer(text="Try again ")
            await ctx.send(embed=wikierror)
        except:
            await ctx.send("bot: Missing argument or permissions to do the command")

    @commands.command(
        slash_interaction=True,
        message_command=True,
        description="Shows information about bot and its author",
    )
    async def about(self, ctx: Context) -> NoReturn:
        """


        Shows a short description of the bot.

        """

        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        ramUsage = self.process.memory_full_info().rss / 1024**2
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        servercount = len(self.bot.guilds)
        usercount = len(self.bot.users)
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title=STRINGS["general"]["abouttitle"],
            description=STRINGS["general"]["aboutdesc"],
            color=0xFF6900,
        )

        embed.add_field(
            name=STRINGS["general"]["aboutver"],
            value=f"```Bot Version: {ver}\nPython Version:{pythonVersion}\nLibrary: discord.py\ndiscord.Py Version: {dpyVersion} ```",
            inline=False,
        )
        embed.add_field(
            name="Other Information",
            value=f"```Server Count: {servercount}\nUser Count: {usercount}\nRAM Usage:{ramUsage:.2f} MB\nDays: {days}d\nHours: {hours}h\nMinutes: {minutes}m\nSeconds: {seconds}s```",
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["aboutauthor"],
            value=STRINGS["general"]["aboutauthortext"],
            inline=True,
        )

        # embed.add_field(name=STRINGS['general']['aboutthanks'], value=STRINGS['general']['aboutthankstext'],inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(
        slash_interaction=True,
        message_command=True,
        description="Shows bot privacy policy",
    )
    async def privacy(self, ctx: Context):
        """


        Shows the privacy policy of the bot

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embed = discord.Embed(
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
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(General(bot))
    Logger.cog_loaded(bot.get_cog("General").name)
