"""This class contains various event listeners for the Discord bot.

The `Listeners` class is a Disnake extension that handles various events that occur in the Discord bot, such as when the bot joins a new guild, when a command is used, when a message is received, and when an error occurs.

The `on_guild_join` event listener sends a welcome message to the first channel in the guild where the bot has permission to send messages. The message includes information about the bot, such as its version and the invite link for the guild.

The `on_command` event listener logs information about commands that are used, including the user who used the command and the guild where it was used.

The `on_message` event listener checks if the bot was mentioned in a message, and if so, it sends a message with the bot's prefix.

The `on_command_error` event listener handles various types of errors that can occur when a command is used, such as missing required arguments, missing permissions, and cooldowns. It logs information about the error and sends an error message to the user.
"""

# -*- coding: utf-8 -*-
import asyncio
import datetime
import os
import traceback
from types import TracebackType
from typing import NoReturn, Union

import disnake
from disnake import Guild, Message
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from termcolor import cprint

from listener.utils import Commands, Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Listeners(commands.Cog, name="Listeners"):
    """ """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Listeners"
        self.logpath = "logs/log.txt"
        self._ensure_log_file_exists()

    def _ensure_log_file_exists(self):
        """ """
        os.makedirs(os.path.dirname(self.logpath), exist_ok=True)
        if not os.path.exists(self.logpath):
            with open(self.logpath, "a", encoding="utf-8") as file:
                pass

    def _log_to_file(self, message: str):
        """

        :param message: str:

        """
        with open(self.logpath, "a", encoding="utf-8") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {message}\n")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild) -> NoReturn:
        """This function sends a welcome message from the bot to the first channel
        in which the bot has the permission to send messages.

        """

        STRINGS = Strings(CONFIG["default_locale"])
        cprint(
            f"""
        ║==============================║
        ║Bot has been added to: {guild}║
        ║==============================║
        """
        )
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        channel = guild.text_channels[0]
        invite = await channel.create_invite()
        embed = disnake.Embed(
            title=STRINGS["general"]["abouttitle"],
            description=STRINGS["general"]["aboutdesc"],
            color=0xFF6900,
        )
        embed.add_field(name=STRINGS["general"]["aboutver"], value=ver, inline=True)
        embed.add_field(
            name=STRINGS["general"]["aboutauthoroninvitetitle"],
            value=STRINGS["general"]["aboutauthoroninvite"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["abouthosting"],
            value=STRINGS["general"]["abouthostingvalue"],
            inline=True,
        )
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        print("The invite for this server is :")
        print(f"{invite}")
        self._log_to_file(f"Bot has been added to: {guild}")
        self._log_to_file(f"The invite for this server is: {invite}")
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_command(self, ctx: Context) -> NoReturn:
        """Logging commands to the console."""
        Logger.command_used(ctx.message.author, ctx.command.name, ctx.message.guild)
        self._log_to_file(
            f"Command used: {ctx.command.name} by {ctx.message.author} in {ctx.message.guild}"
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> NoReturn:
        """Getting the bot prefix when it is mentioned."""
        try:
            s = await Settings(self.ctx.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            prefix = await s.get_field("prefix", CONFIG["default_prefix"])
            STRINGS = Strings(lang)
        except AttributeError:
            pass
        else:
            if message.content in [
                f"<@!{self.bot.user.id}>",
                f"<@{self.bot.user.id}>",
                f"@{self.bot.user}",
            ]:
                await message.channel.send(
                    STRINGS["etc"]["on_mention"].format(message.author.id, prefix)
                )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> NoReturn:
        await self.handle_error(ctx, error)

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: Exception
    ) -> NoReturn:
        await self.handle_error(inter, error)

    async def handle_error(
            self,
            ctx_or_inter: Union[Context, disnake.ApplicationCommandInteraction],
            error: Exception,
        ) -> NoReturn:
            """
            If an unexpected error occurs, it displays an error message with relevant information about the error, such as the guild, member, command, and the full traceback.
            
            Args:
                ctx_or_inter (Union[Context, disnake.ApplicationCommandInteraction]): The context or interaction object associated with the command that caused the error.
                error (Exception): The exception object that represents the error that occurred.
            
            Returns:
                NoReturn: This function does not return anything.
            """
            
            
            s = await Settings(ctx_or_inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            COMMANDS = Commands(lang)

            command_name = ctx_or_inter.application_command.name if hasattr(ctx_or_inter, 'application_command') else ctx_or_inter.command.name if ctx_or_inter.command else 'Unknown'

            error_message = f"""
            ║========================║=========================║
            ║ Guild                  ║ Member                  ║
            ║{ctx_or_inter.guild.name}:║ {ctx_or_inter.author.name}:::::::::::::::::║
            ║========================║=========================║
            ║ Guild ID               ║ Member ID               ║
            ║ {ctx_or_inter.guild.id}:::::║ {ctx_or_inter.author.id}::::::║
            ║========================║=========================║
            ║ Command                ║
            ║ {command_name}::::::::::::::::::::::::::::::::::::║
            ║========================║
            =======================================================
            Traceback
            {traceback.format_exception(type(error), error, error.__traceback__)}
            =======================================================
            """
            cprint("==============================")
            cprint(error_message, color="red")
            cprint("==============================")
            self._log_to_file(error_message)

            if isinstance(error, commands.CommandNotFound):
                return

            if isinstance(error, commands.MissingRequiredArgument):
                prefix = await s.get_field("prefix", CONFIG["default_prefix"])

            if ctx_or_inter.application_command and ctx_or_inter.application_command.cog and ctx_or_inter.application_command.cog.name != "Jishaku":
                cog_name = ctx_or_inter.application_command.cog.name
                if cog_name in COMMANDS and command_name in COMMANDS[cog_name]["commands"]:
                    embed = Utils.error_embed(
                        STRINGS["etc"]["usage"].format(
                            COMMANDS[cog_name]["commands"][command_name]["usage"].format(prefix)
                        )
                    )
                else:
                    embed = Utils.error_embed(STRINGS["error"]["command_not_found"])
            elif isinstance(error, commands.MissingPermissions):
                embed = Utils.error_embed(STRINGS["error"]["missing_perms"])

            elif isinstance(error, commands.BotMissingPermissions):
                embed = Utils.error_embed(
                STRINGS["error"]["missing_bot_perms"].format(
                    " ".join(
                        "+ " + STRINGS["etc"]["permissions"][f"{perm}"]
                        for perm in error.missing_permissions
                    )
                )
            )

            elif isinstance(error, commands.CommandOnCooldown):
                embed = Utils.error_embed(
                    STRINGS["error"]["cooldown"].format(error.retry_after)
                )

            elif isinstance(error, commands.errors.NSFWChannelRequired):
                embed = disnake.Embed(
                    title=STRINGS["error"]["nsfwerrortitle"],
                    description=STRINGS["error"]["nsfwnotcorrectspot"],
                    color=0xFF0000,
                )
                embed.add_field(
                    name=STRINGS["error"]["nsfwlogerror"],
                    value=STRINGS["error"]["nsfwtraceback"].format(str(error)),
                    inline=False,
                )

            else:
                embed = disnake.Embed(color=0xDD0000)
                embed.title = STRINGS["error"]["on_error_title"]
                embed.description = STRINGS["error"]["on_error_text"].format(str(error))

            if isinstance(ctx_or_inter, Context):
                msg = await ctx_or_inter.send(embed=embed)
                await asyncio.sleep(20)
                await msg.delete()
            else:
                await ctx_or_inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot: Bot) -> NoReturn:
    """

    :param bot: Bot:

    """
    bot.add_cog(Listeners(bot))

    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    Logger.cog_loaded(bot.get_cog("Listeners").name)
