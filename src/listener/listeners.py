# -*- coding: utf-8 -*-
import asyncio
import datetime
from typing import NoReturn

import disnake
from disnake import Guild, Message
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from termcolor import cprint

from listener.utils import Commands, Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Listeners(commands.Cog, name="Listeners"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Listeners"

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
        logpath = "logs/log.txt"
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
        # embed.add_field(name=STRINGS['general']['aboutthanks'], value=STRINGS['general']['aboutthankstext'],inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        print("The invite for this server is :")
        print(f"{invite}")
        with open(logpath, "a") as file:
            print("\n", file=file)
            print(f"Bot has been added to: {guild}", file=file)
            print("The invite for this server is :", file=file)
            print(f"{invite}", file=file)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_command(self, ctx: Context) -> NoReturn:
        """Logging commands to the console."""
        Logger.command_used(ctx.message.author, ctx.command.name, ctx.message.guild)

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
        """If an unexpected error occurs, it displays an... error message?

        Attributes:
        -----------
        - `error` - error information

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        COMMANDS = Commands(lang)
        logpath = "logs/log.txt"
        cprint("==============================")
        cprint(
            f"""
        ║========================║=========================║
        ║ Guild                  ║ Member                  ║
        ║ {ctx.guild.name}::::::::::::::║ {ctx.author.name}:::::::::::::::::║        
        ║========================║=========================║
        ║ Guild ID               ║ Member ID               ║
        ║ {ctx.guild.id}:::::║ {ctx.author.id}::::::║
        ║========================║=========================║
        =======================================================
        Traceback 
        {error}
        =======================================================
        """
        )
        cprint("==============================")
        with open(logpath, "a") as file:
            print("\n", file=file)
            print("An error has occured in the bot!", file=file)
            print(f"Traceback : {error}", file=file)
            print(
                f"Guild that caused the error : {ctx.guild.name} - Guild id {ctx.guild.id} - Member triggering the error {ctx.author.name} - Member id {ctx.author.id} ",
                file=file,
            )

        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.message.add_reaction(CONFIG["no_emoji"])

        if isinstance(error, commands.MissingRequiredArgument):
            prefix = await s.get_field("prefix", CONFIG["default_prefix"])

            if ctx.command.cog.name != "Jishaku":
                embed = Utils.error_embed(
                    STRINGS["etc"]["usage"].format(
                        COMMANDS[ctx.command.cog.name]["commands"][ctx.command.name][
                            "usage"
                        ].format(prefix)
                    )
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = Utils.error_embed(STRINGS["error"]["missing_perms"])

        elif isinstance(error, commands.BotMissingPermissions):
            embed = Utils.error_embed(
                STRINGS["error"]["missing_bot_perms"].format(
                    " ".join(
                        "+ " + STRINGS["etc"]["permissions"][f"{perm}"]
                        for perm in error.missing_perms
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
            # Logger.warn(str(error))

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(20)
        await msg.delete()


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Listeners(bot))

    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    Logger.cog_loaded(bot.get_cog("Listeners").name)
