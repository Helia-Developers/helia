"""
A module required to administer the bot. Only works for its owners.

This module provides commands for loading, unloading, and reloading bot modules (cogs), as well as commands for shutting down the bot, setting the bot's status, and generating bot invite links.

The module also includes a custom `Confirm` view that is used to confirm the shutdown command.

Only bot owners are allowed to use the commands in this module.
"""

# -*- coding: utf-8 -*-
import asyncio
import datetime
import os
import typing
from os import system as sys
from os.path import abspath, dirname
from typing import NoReturn
import json

import disnake
from disnake import ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from disnake.ext.commands.params import Param
from disnake.ui import Button, Select, View
from dotenv import load_dotenv

from listener.utils import Config, Logger, Settings, Strings, Utils

# from disnake_components import Button, ButtonStyle, disnakeComponents

# from disnake.ext.commands import Bot, Context

CONFIG = Config()
# STRINGS = Strings(CONFIG["default_locale"])

# Load valid users from JSON config
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    valid_users = config.get('valid_users', [])

class Confirm(disnake.ui.View):
    def __init__(self, ctx, bot: Bot):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @disnake.ui.button(style=ButtonStyle.green, label="✓", custom_id="yes")
    async def confirm(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        s = await Settings(self.ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        if isinstance(self.ctx, disnake.ApplicationCommandInteraction):
            author = self.ctx.author
        else:
            author = self.ctx.message.author

        if str(author.id) in valid_users:
            await interaction.response.edit_message(
                embed=disnake.Embed(
                    title=STRINGS["moderation"]["shutdownembedtitle"],
                    description=STRINGS["moderation"]["shutdownembeddesc"],
                    color=0xFF8000,
                ),
                view=None,
            )
            await self.bot.change_presence(
                status=disnake.Status.online,
                activity=disnake.Game(
                    name="Shutting down for either reboot or update "
                ),
            )
            await asyncio.sleep(5)
            print("---------------------------")
            print("[SHUTDOWN] Shutdown requested by bot owner")
            print("---------------------------")
            await self.bot.close()
        else:
            await interaction.response.edit_message(
                embed=disnake.Embed(
                    title=STRINGS["moderation"]["shutdownaborttitle"],
                    description=STRINGS["moderation"]["shutdownabortdesc"],
                    color=0xDD2E44,
                ),
                view=None,
            )
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @disnake.ui.button(style=ButtonStyle.red, label="X", custom_id="no")
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        s = await Settings(self.ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        if isinstance(self.ctx, disnake.ApplicationCommandInteraction):
            author = self.ctx.author
        else:
            author = self.ctx.message.author
        await interaction.response.edit_message(
            embed=disnake.Embed(
                title=STRINGS["moderation"]["shutdownaborttitle"],
                description=STRINGS["moderation"]["shutdownabortdesc"],
                color=0xDD2E44,
            ),
            view=None,
        )
        self.value = False
        self.stop()


class Admin(commands.Cog, name="Admin"):
    """A module required to administer the bot. Only works for its owners."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Admin"

    # ... [rest of the code remains unchanged]
    @commands.command(slash_command=True, message_command=True)
    @commands.is_owner()
    async def load(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f"listener.{module}")
            embeder = disnake.Embed(
                title=f"Module {module} has been loaded", color=0x0C0C0C
            )
            await ctx.send(embed=embeder, delete_after=5)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        # else:
        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.slash_command(
        name="load",
        description="Load a module.",
    )
    @commands.is_owner()
    async def sload(
        self,
        inter: disnake.ApplicationCommandInteraction,
        *,
        module: str = Param(description="Name of the module."),
    ) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f"listener.{module}")
            embeder = disnake.Embed(
                title=f"Module {module} has been loaded", color=0x0C0C0C
            )
            await inter.response.send_message(embed=embeder, ephemeral=True)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed(f"`{type(e).__name__}`: {e}")
            await inter.response.send_message(embed=embed)
        # else:
        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True, message_command=True)
    @commands.is_owner()
    async def unload(self, ctx: Context, *, module: str) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f"listener.{module}")
            embederx = disnake.Embed(
                title=f"Module {module} has been unloaded", color=0x0C0C0C
            )
            await ctx.send(embed=embederx, delete_after=5)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        # else:

        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.slash_command(
        name="unload",
        description="Unload a module.",
    )
    @commands.is_owner()
    async def sunload(
        self,
        inter: disnake.ApplicationCommandInteraction,
        *,
        module: str = Param(description="Name of the module."),
    ) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f"listener.{module}")
            embederx = disnake.Embed(
                title=f"Module {module} has been unloaded", color=0x0C0C0C
            )
            await inter.response.send_message(embed=embederx, ephemeral=True)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await inter.response.send_message(embed=embed)
        # else:

        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(slash_command=True, message_command=True, name="reload")
    @commands.is_owner()
    async def _reload(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f"listener.{module}")
            embederxx = disnake.Embed(
                title=f"Module {module} has been reloaded", color=0x0C0C0C
            )
            await ctx.send(embed=embederxx, delete_after=5)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await ctx.send(embed=embed)
        # else:
        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.slash_command(
        name="reload",
        description="Reload a module.",
    )
    @commands.is_owner()
    async def _sreload(
        self,
        inter: disnake.ApplicationCommandInteraction,
        *,
        module: str = Param(description="Name of the module."),
    ) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f"listener.{module}")
            embederxx = disnake.Embed(
                title=f"Module {module} has been reloaded", color=0x0C0C0C
            )
            await inter.response.send_message(embed=embederxx, ephemeral=True)
        except Exception as e:
            # await ctx.message.add_reaction(CONFIG["no_emoji"])
            embed = Utils.error_embed("`{}`: {}".format(type(e).__name__, e))
            await inter.response.send_message(embed=embed)
        # else:
        # await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command(
        slash_command=True,
        message_command=True,
        name="invite_bot",
        brief="Makes a bot invite without any permissions",
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def invite_bot(self, ctx, *, user: typing.Optional[disnake.User] = None):
        user = user or ctx.author

        if not user.bot:
            embed = disnake.Embed(
                title="Error",
                description="The provided user id is not a bot!",
                color=0xFF0000,
            )

            return await ctx.send(embed=embed)

        invite = disnake.utils.oauth_url(
            client_id=user.id, scopes=("bot", "applications.commands")
        )
        embeder = disnake.Embed(
            title="Generating invite for the provided user id", color=0x778EFD
        )
        waiter = await ctx.send(embed=embeder, delete_after=5)
        await asyncio.sleep(5)
        embedtimes = disnake.Embed(title="Your invite", color=0x778EFD)
        embedtimes.add_field(name="Is here", value=f"{invite}", inline=True)
        await ctx.send(embed=embedtimes)

    @commands.slash_command(
        name="invite_bot",
        description="Makes a bot invite without any permissions.",
    )
    async def sinvite_bot(
        self, inter: disnake.ApplicationCommandInteraction, *, user: disnake.User = None
    ):
        user = user or inter.author

        if not user.bot:
            embed = disnake.Embed(
                title="Error",
                description="The provided user id is not a bot!",
                color=0xFF0000,
            )

            return await inter.response.send_message(embed=embed)

        invite = disnake.utils.oauth_url(
            client_id=user.id, scopes=("bot", "applications.commands")
        )
        embeder = disnake.Embed(
            title="Generating invite for the provided user id", color=0x778EFD
        )

        embedtimes = disnake.Embed(title="Your invite is here", color=0x778EFD)
        embedtimes.add_field(name="Link", value=f"{invite}", inline=True)
        await inter.response.send_message(embed=embedtimes, ephemeral=True)



    @commands.slash_command(
        name="set_status",
        description="Set the bot status[OWNERS-ONLY!!!!].",
    )
    async def slashset_status(
        self,
        inter: disnake.ApplicationCommandInteraction,
        sts: str = Param(description="Text of status."),
    ):
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = inter.author
        
        if str(author.id) in valid_users:
            await self.bot.change_presence(activity=disnake.Game(" ".join(sts)))
            embed = disnake.Embed(
                title=STRINGS["moderation"]["setstatustext"],
                description=STRINGS["moderation"]["setstatusdesc"],
                color=0xFF8000,
            )
            embed.add_field(
                name=STRINGS["moderation"]["setstatusfieldtext"],
                value=STRINGS["moderation"]["setstatusfielddesc"],
                inline=True,
            )
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        else:
            embed = disnake.Embed(
                title="You failed",
                description="Need Permission : Bot Owner",
                color=0xFF0000,
            )

        await inter.response.send_message(embed=embed)

    @commands.command(description="Bot restart")
    @commands.is_owner()
    async def restart(self, ctx):
        for ext in self.bot.cogs:  # Idk how you called it
            self.bot.reload_extension(f"{ext}")

    @commands.command(
        slash_command=True, message_command=True, description="Bot invite links"
    )
    async def invite(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        view = disnake.ui.View()
        viewx = disnake.ui.View()
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitetitle"],
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitedescd"],
                url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["canaryver"],
                url="https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupsdc"],
                url=f"https://bots.server-discord.com/{self.bot.user.id}",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botuptopgg"],
                url=f"https://top.gg/bot/{self.bot.user.id}",
            )
        )
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupbod"],
                url=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
            )
        )
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupdblco"],
                url=f"https://discordbotslist.co/bot/{self.bot.user.id}",
            )
        )
        embed = disnake.Embed(
            title=STRINGS["general"]["invitedescd"],
            colour=disnake.Colour(0xFF6900),
            # url=
            # f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            description=STRINGS["general"]["botinvitedesc"],
        )
        # embed.set_author(
        # name=STRINGS["general"]["botinvitedescd"],
        # url=
        # f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
        # )
        # mostly useful for helia canary invite but still why not have it be there - comment if your self hosted version will not have canary branch
        # embed.add_field(
        # name=STRINGS["general"]["canaryver"],
        # value=
        # f"https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
        # inline=False,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupsdc"],
        # value=f"https://bots.server-discord.com/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botuptopgg"],
        # value=f"https://top.gg/bot/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupbod"],
        # value=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupdblco"],
        # value=f"https://discordbotslist.co/bot/{self.bot.user.id}",
        # inline=True,
        # )
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        embedcont = disnake.Embed(title="-----", colour=disnake.Colour(0xFF6900))
        await ctx.send(embed=embed, view=view)
        await ctx.send("`----`", view=viewx)

    @commands.slash_command(
        name="invite",
        description="Bot invite links.",
    )
    async def slashinvite(self, inter: disnake.ApplicationCommandInteraction):
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        view = disnake.ui.View()
        viewx = disnake.ui.View()
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitetitle"],
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botinvitedescd"],
                url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["canaryver"],
                url="https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupsdc"],
                url=f"https://bots.server-discord.com/{self.bot.user.id}",
            )
        )
        view.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botuptopgg"],
                url=f"https://top.gg/bot/{self.bot.user.id}",
            )
        )
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupbod"],
                url=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
            )
        )
        viewx.add_item(
            Button(
                style=ButtonStyle.link,
                label=STRINGS["general"]["botupdblco"],
                url=f"https://discordbotslist.co/bot/{self.bot.user.id}",
            )
        )
        embed = disnake.Embed(
            title=STRINGS["general"]["invitedescd"],
            colour=disnake.Colour(0xFF6900),
            # url=
            # f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=204859462&scope=applications.commands%20bot",
            description=STRINGS["general"]["botinvitedesc"],
        )
        # embed.set_author(
        # name=STRINGS["general"]["botinvitedescd"],
        # url=
        # f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=204557314",
        # )
        # mostly useful for helia canary invite but still why not have it be there - comment if your self hosted version will not have canary branch
        # embed.add_field(
        # name=STRINGS["general"]["canaryver"],
        # value=
        # f"https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",
        # inline=False,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupsdc"],
        # value=f"https://bots.server-discord.com/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botuptopgg"],
        # value=f"https://top.gg/bot/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupbod"],
        # value=f"https://bots.ondiscord.xyz/bots/{self.bot.user.id}",
        # inline=True,
        # )
        # embed.add_field(
        # name=STRINGS["general"]["botupdblco"],
        # value=f"https://discordbotslist.co/bot/{self.bot.user.id}",
        # inline=True,
        # )
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        embedcont = disnake.Embed(title="-----", colour=disnake.Colour(0xFF6900))
        await inter.response.send_message(embed=embed, view=view)
        await inter.response.send_message("`----`", view=viewx)

    @commands.command(
        slash_command=True, message_command=True, brief="Gives the bot's uptime"
    )
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = disnake.Embed(title="Bot uptime")
        embed.add_field(name="Days", value=f"```{days}d```", inline=True)
        embed.add_field(name="Hours", value=f"```{hours}h```", inline=True)
        embed.add_field(name="Minutes", value=f"```{minutes}m```", inline=False)
        embed.add_field(name="Seconds", value=f"```{seconds}s```", inline=False)
        await ctx.send(embed=embed)

    @commands.slash_command(
        name="uptime",
        description="Bot uptime.",
    )
    async def slashuptime(self, inter: disnake.ApplicationCommandInteraction):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = disnake.Embed(title="Bot uptime")
        embed.add_field(name="Days", value=f"```{days}d```", inline=True)
        embed.add_field(name="Hours", value=f"```{hours}h```", inline=True)
        embed.add_field(name="Minutes", value=f"```{minutes}m```", inline=False)
        embed.add_field(name="Seconds", value=f"```{seconds}s```", inline=False)
        await inter.response.send_message(embed=embed)

    @commands.command(
        slash_command=True, message_command=True, name="shutdown",
        description="Bot restart/shutdown",
    )
    async def shutdown(self, ctx: Context):  # Команда для выключения бота
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = ctx.message.author
        viewb = Confirm(ctx, self.bot)
        viewbx = disnake.ui.View()

        viewbx.add_item(Button(style=ButtonStyle.grey, label="·", disabled=True))
        embedconfirm = disnake.Embed(
            title=STRINGS["moderation"]["shutdownembedtitle"],
            description=STRINGS["moderation"]["shutdownconfirm"],
        )
        await ctx.send(embed=embedconfirm, view=viewb)
        await viewb.wait()

    @commands.slash_command(
        name="shutdown",
        description="Shutdown the bot [OWNERS-ONLY!!!!].",
    )
    async def slashshutdown(
        self, inter: disnake.ApplicationCommandInteraction
    ):  # Команда для выключения бота
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = inter.author
        viewb = Confirm(inter, self.bot)
        viewbx = disnake.ui.View()

        viewbx.add_item(Button(style=ButtonStyle.grey, label="·", disabled=True))
        embedconfirm = disnake.Embed(
            title=STRINGS["moderation"]["shutdownembedtitle"],
            description=STRINGS["moderation"]["shutdownconfirm"],
        )
        await inter.response.send_message(embed=embedconfirm, view=viewb)
        await viewb.wait()

    @commands.command(
        slash_command=True, message_command=True, description="Set bot status"
    )
    async def set_status(self, ctx, *args):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        author = ctx.message.author
        if str(author.id) in valid_users:
            await self.bot.change_presence(activity=disnake.Game(" ".join(args)))
            embed = disnake.Embed(
                title=STRINGS["moderation"]["setstatustext"],
                description=STRINGS["moderation"]["setstatusdesc"],
                color=0xFF8000,
            )
            embed.add_field(
                name=STRINGS["moderation"]["setstatusfieldtext"],
                value=STRINGS["moderation"]["setstatusfielddesc"],
                inline=True,
            )
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        else:
            embed = disnake.Embed(
                title="You failed",
                description="Need Permission : Bot Owner",
                color=0xFF0000,
            )

        await ctx.send(embed=embed)

    # ... [rest of the code remains unchanged]

def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Admin(bot))
    Logger.cog_loaded(bot.get_cog("Admin").name)
