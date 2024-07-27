# remove .removethisforenable in file name for this cog to load
import asyncio
import functools
import os
import sqlite3

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from termcolor import cprint

from scripts import db


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logpath = "logs/log.txt"
        # with open(path, "r") as file:
        # ver = file.readline()

        cprint(
            f"""
        ║============================================================║
        ║-------- {member} joined {member.guild.name}-----------------------║
        ║============================================================║
        """
        )
        with open(logpath, "a") as file:
            print("\n", file=file)
            print(f"{member} joined {member.guild.name}", file=file)

        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("welcome", "channel_id", "guild_id", member.guild.id)
        )
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return

        cursor.execute(db.select_table("welcome", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        hello = disnake.Embed(
            title="User joined the server",
            description=f"```Welcome {member} to {member.guild}```",
        )
        hello.set_author(name="Welcome System")
        if desc is None:
            descdef = "Give them a warm welcome and say hello to them"

            hello.add_field(
                name="Server message", value=f"```{descdef}```", inline=True
            )
        else:
            hello.add_field(
                name="Server message", value=f"```{desc[0]}```", inline=True
            )

        channel = self.bot.get_channel(int(chan[0]))
        await channel.send(embed=hello)
        cursor.close()
        connect.close()

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx: Context):
        descwelcgood = """
                Here is the list of commands related to server join and leave messages
                ```welcome - Displays this message```
                .
                ```welcome channel [#channel mention] - Set welcome channel```
                .
                ```welcome clear - Remove the set welcome channel```
                .
                ```welcome text {Optionally enter text - otherwise the default will be set} - Set welcome text```
                .
                ```goodbye - Displays this message```
                .
                ```goodbye channel [#channel mention] - Set goodbye channel```
                .
                ```goodbye clear - Remove the set goodbye channel```
                .
                ```goodbye text {Optionally enter text - otherwise the default will be set} - Set goodbye text```

                """
        welcomehelp = disnake.Embed(
            title=":wave: Welcome & Goodbye Messages",
            description=f"{descwelcgood}",
        ).set_author(name="Help System")
        await ctx.send(embed=welcomehelp)

    @welcome.command(pass_context=True)
    async def channel(self, ctx: Context, chan: disnake.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table(
                        "welcome", "channel_id", "guild_id", ctx.message.guild.id
                    )
                )
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, chan.id)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "channel_id"), val
                    )
                else:
                    cursor.execute(
                        db.update_table(
                            "welcome",
                            "channel_id",
                            chan.id,
                            "guild_id",
                            ctx.message.guild.id,
                        )
                    )
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(
                    f"Set the welcome channel in guild {ctx.message.guild} to {chan.mention} ,the id of it being {chan.id} and id of guild being {ctx.message.guild.id}"
                )
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Failed to set channel")

    @welcome.command(pass_context=True)
    async def clear(self, ctx: Context):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table(
                        "welcome", "channel_id", "guild_id", ctx.message.guild.id
                    )
                )
                res = cursor.fetchone()
                if res is None:
                    await ctx.send(
                        " Do not have a table for the welcome channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("welcome", "guild_id", ctx.message.guild.id)
                    )
                    await ctx.send(" Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Failed to remove welcome channel setting")

    @welcome.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                if content is None:
                    await ctx.send("Setting default message")
                    content = "Give them a warm welcome and say hello to them"
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "text", "guild_id", ctx.message.guild.id)
                )
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(db.insert_table("welcome", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE welcome SET text = ? WHERE guild_id = ?", val
                    )
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send("Set the welcome message text")
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("Error , argument may be invalid")


def setup(bot):
    bot.add_cog(Welcome(bot))
