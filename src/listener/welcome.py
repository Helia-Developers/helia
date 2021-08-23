# remove .removethisforenable in file name for this cog to load
import asyncio
import functools
import os
import sqlite3

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from scripts import db


class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("welcome", "channel_id", "guild_id",
                            member.guild.id))
        chan = cursor.fetchone()
        # print(f" Channel id fetch - {chan[0]}")
        if chan is None:
            return

        else:
            cursor.execute(
                db.select_table("welcome", "text", "guild_id",
                                member.guild.id))
            desc = cursor.fetchone()
            descdef = f"Give him a warm welcome and say hello to him"
                
            hello = discord.Embed(title="User joined the server",
                                  description="Details Below")
            hello.set_author(name="Welcome System")
            hello.add_field(name=f"Welcome {member}",
                            value=f" to {member.guild} ",
                            inline=True)
            if desc == None:
                hello.add_field(name="Server message", value=f"{descdef}", inline=True)
            else:
                hello.add_field(name="Server message", value=desc[0], inline=True)
                
            

            channel = self.bot.get_channel(id=int(chan[0]))
            await channel.send(embed=hello)
        cursor.close()
        connect.close()

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx: Context):
        await ctx.send("No help information temporarily")

    @welcome.command(pass_context=True)
    async def channel(self, ctx: Context, chan: discord.TextChannel = None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, chan.id)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "channel_id"),
                        val)
                else:
                    cursor.execute(
                        db.update_table(
                            "welcome",
                            "channel_id",
                            chan.id,
                            "guild_id",
                            ctx.message.guild.id,
                        ))
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
                    db.select_table("welcome", "channel_id", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    await ctx.send(
                        "bot: Do not have a table for the welcome channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("welcome", "guild_id",
                                        ctx.message.guild.id))
                    await ctx.send("bot: Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await ctx.send(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("bot: Error")

    @welcome.command(pass_context=True)
    async def text(self, ctx: Context, *, content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.manage_channels:
                if content is None:
                    await ctx.send(
                        "Setting default message"
                    )
                    content = "Give him a warm welcome and say hello to him"
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "text", "guild_id",
                                    ctx.message.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.message.guild.id, content)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "text"), val)
                else:
                    val = (content, ctx.message.guild.id)
                    cursor.execute(
                        "UPDATE welcome SET text = ? WHERE guild_id = ?", val)
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send("bot: Set the welcome message text")
            else:
                await ctx.send(
                    "bot: You do not have enough permissions - :You require **Manage Channels**."
                )
        except:
            await ctx.send("bot: Error , argument may be invalid")


def setup(bot):
    bot.add_cog(welcome(bot))
