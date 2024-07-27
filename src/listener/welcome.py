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

        cprint(f"""
        ║============================================================║
        ║-------- {member} joined {member.guild.name}-----------------------║
        ║============================================================║
        """)
        with open(logpath, "a") as file:
            print("\n", file=file)
            print(f"{member} joined {member.guild.name}", file=file)

        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("welcome", "channel_id", "guild_id",
                            member.guild.id))
        chan = cursor.fetchone()
        if chan is None:
            return

        cursor.execute(
            db.select_table("welcome", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        hello = disnake.Embed(
            title="User joined the server",
            description=f" {member} to {member.guild}",
        )
        hello.set_author(name="Welcome System")
        if desc is None:
            descdef = "Give them a warm welcome and say hello to them"

            hello.add_field(name="Server message",
                            value=f"{descdef}",
                            inline=True)
        else:
            hello.add_field(name="Server message",
                            value=f"{desc[0]}",
                            inline=True)

        channel = self.bot.get_channel(int(chan[0]))
        await channel.send(embed=hello)
        cursor.close()
        connect.close()

    @commands.slash_command(name="welcome", description="Welcome commands")
    async def welcome(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays the list of commands related to server join and leave messages.
        """
        descwelcgood = """
                Here is the list of commands related to server join and leave messages
                /welcome - Displays this message
                .
                /welcome channel [#channel mention] - Set welcome channel
                .
                /welcome clear - Remove the set welcome channel
                .
                /welcome text {Optionally enter text - otherwise the default will be set} - Set welcome text
                .
                /goodbye - Displays this message
                .
                /goodbye channel [#channel mention] - Set goodbye channel
                .
                /goodbye clear - Remove the set goodbye channel
                .
                /goodbye text {Optionally enter text - otherwise the default will be set} - Set goodbye text

                """
        welcomehelp = disnake.Embed(
            title=":wave: Welcome & Goodbye Messages",
            description=f"{descwelcgood}",
        ).set_author(name="Help System")
        await inter.response.send_message(embed=welcomehelp)

    @welcome.sub_command(name="channel", description="Set welcome channel")
    async def channel(self, inter: disnake.ApplicationCommandInteraction, chan: disnake.TextChannel):
        """
        Set the welcome channel for the server.

        Parameters:
        -----------
        chan: disnake.TextChannel
            The channel to set as the welcome channel.
        """
        try:
            if inter.author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "channel_id", "guild_id",
                                    inter.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (inter.guild.id, chan.id)
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
                            inter.guild.id,
                        ))
                connect.commit()
                cursor.close()
                connect.close()
                await inter.response.send_message(
                    f"Set the welcome channel in guild {inter.guild} to {chan.mention} ,the id of it being {chan.id} and id of guild being {inter.guild.id}"
                )
            else:
                await inter.response.send_message(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except Exception as e:
            await inter.response.send_message(f"Failed to set channel: {str(e)}")

    @welcome.sub_command(name="clear", description="Remove the set welcome channel")
    async def clear(self, inter: disnake.ApplicationCommandInteraction):
        """
        Remove the set welcome channel for the server.
        """
        try:
            if inter.author.guild_permissions.manage_channels:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "channel_id", "guild_id",
                                    inter.guild.id))
                res = cursor.fetchone()
                if res is None:
                    await inter.response.send_message(
                        "Do not have a table for the welcome channel - Check Database."
                    )
                else:
                    cursor.execute(
                        db.delete_table("welcome", "guild_id",
                                        inter.guild.id))
                    await inter.response.send_message("Cleared the table")
                connect.commit()
                cursor.close()
                connect.close()
            else:
                await inter.response.send_message(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except Exception as e:
            await inter.response.send_message(f"Failed to remove welcome channel setting: {str(e)}")

    @welcome.sub_command(name="text", description="Set welcome message text")
    async def text(self, inter: disnake.ApplicationCommandInteraction, content: str = None):
        """
        Set the welcome message text for the server.

        Parameters:
        -----------
        content: str, optional
            The welcome message text to set. If not provided, a default message will be used.
        """
        try:
            if inter.author.guild_permissions.manage_channels:
                if content is None:
                    await inter.response.send_message("Setting default message")
                    content = "Give them a warm welcome and say hello to them"
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(
                    db.select_table("welcome", "text", "guild_id",
                                    inter.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (inter.guild.id, content)
                    cursor.execute(
                        db.insert_table("welcome", "guild_id", "text"), val)
                else:
                    val = (content, inter.guild.id)
                    cursor.execute(
                        "UPDATE welcome SET text = ? WHERE guild_id = ?", val)
                connect.commit()
                cursor.close()
                connect.close()
                await inter.response.send_message("Set the welcome message text")
            else:
                await inter.response.send_message(
                    "You do not have enough permissions - :You require **Manage Channels**."
                )
        except Exception as e:
            await inter.response.send_message(f"Error, argument may be invalid: {str(e)}")


def setup(bot):
    bot.add_cog(Welcome(bot))
