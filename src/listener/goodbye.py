# remove .removethisforenable in file name for this cog to load
import asyncio
import functools
import sqlite3
from datetime import datetime

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from termcolor import cprint

from scripts import db


class Goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logpath = "logs/log.txt"
        # with open(path, "r") as file:
        # ver = file.readline()
        cprint(
            f"""
        ║============================================================║
        ║-------- {member} left {member.guild.name}-----------------------║
        ║============================================================║
        """
        )
        with open(logpath, "a") as file:
            print("\n", file=file)
            print(f"{member} left {member.guild.name}", file=file)

        # now  = datetime.now()
        # time = now.strftime("%H:%M:%S")
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("goodbye", "channel_id", "guild_id", member.guild.id)
        )
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return
        cursor.execute(db.select_table("goodbye", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        descdef = f"The one who left was {member}, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "
        gb = disnake.Embed(
            title="User left the server",
            description=f"```Someone left {member.guild}```",
        )
        gb.set_author(name="Goodbye System")

        if desc is None:
            gb.add_field(name="Server message", value=f"{descdef}", inline=True)
        else:
            gb.add_field(name="Server message", value=f"```{desc[0]}```", inline=True)
        channel = self.bot.get_channel(int(chan[0]))
        cursor.close()
        connect.close()
        await channel.send(embed=gb)

    @commands.group(invoke_without_command=True)
    async def goodbye(self, ctx: Context):
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
        goodbyehelp = disnake.Embed(
            title=":wave: Welcome & Goodbye Messages",
            description=f"{descwelcgood}",
        ).set_author(name="Help System")
        await ctx.send(embed=goodbyehelp)

    @goodbye.command()
    async def channel(self, ctx: Context, channel: disnake.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table(
                        "goodbye", "channel_id", "guild_id", ctx.message.guild.id
                    )
                )
                result = cursor.fetchone()
                if result is None:
                    val = (ctx.message.guild.id, channel.id)
                    cursor.execute(
                        db.insert_table("goodbye", "guild_id", "channel_id"), val
                    )
                else:
                    cursor.execute(
                        db.update_table(
                            "goodbye",
                            "channel_id",
                            channel.id,
                            "guild_id",
                            ctx.message.guild.id,
                        )
                    )
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(
                    f"Set the goodbye in guild {ctx.message.guild} to {channel.mention} ,the id of it being {channel.id} and id of guild being {ctx.message.guild.id}"
                )
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**"
                )
        except:
            await ctx.send("Failed to set channel")

    @goodbye.command()
    async def clear(self, ctx: Context):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table(
                        "goodbye", "channel_id", "guild_id", ctx.message.guild.id
                    )
                )
                result = cursor.fetchone()
                if result is None:
                    await ctx.send(
                        " Do not have a table for the goodbye channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("goodbye", "guild_id", ctx.message.guild.id)
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
            await ctx.send("Failed to remove goodbye channel setting")

    @goodbye.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                if content is None:
                    await ctx.send("Setting default message")
                    content = "A person left, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "

                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("goodbye", "text", "guild_id", ctx.message.guild.id)
                )
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(db.insert_table("goodbye", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE goodbye SET text = ? WHERE guild_id = ?", val
                    )
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(" Set the goodbye message text")
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send(" Error , argument may be invalid")


def setup(bot):
    bot.add_cog(Goodbye(bot))
