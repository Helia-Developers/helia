"""
The `Goodbye` class is a Discord bot cog that handles member leave events. It logs when a member leaves a server, and sends a customizable goodbye message to a configured channel.

The cog provides the following slash commands:
- `/goodbye`: Displays a help message with all the available goodbye-related commands.
- `/goodbye_channel`: Sets the channel where the goodbye message will be sent.
- `/goodbye_clear`: Removes the configured goodbye channel.
- `/goodbye_text`: Sets the text of the goodbye message.

The `on_member_remove` event listener is responsible for sending the goodbye message when a member leaves the server. It retrieves the configured channel and message from the database, and sends an embed message with the goodbye text.
"""

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
    """ """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logpath = "logs/log.txt"
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

        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(
            db.select_table("goodbye", "channel_id", "guild_id", member.guild.id)
        )
        chan = cursor.fetchone()
        if chan is None:
            return
        cursor.execute(db.select_table("goodbye", "text", "guild_id", member.guild.id))
        desc = cursor.fetchone()
        descdef = f"The one who left was {member}, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "
        gb = disnake.Embed(
            title="User left the server",
            description=f" left {member.guild}",
        )
        gb.set_author(name="Goodbye System")

        if desc is None:
            gb.add_field(name="Server message", value=f"{descdef}", inline=True)
        else:
            gb.add_field(name="Server message", value=f"{desc[0]}", inline=True)
        channel = self.bot.get_channel(int(chan[0]))
        cursor.close()
        connect.close()
        await channel.send(embed=gb)

    @commands.slash_command(name="goodbye", description="Help")
    async def goodbye(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays a help message with all the available goodbye-related commands.
        """
        descwelcgood = """
                Here is the list of commands related to server join and leave messages
                /welcome - Displays this message
                .
                /welcome_channel [#channel mention] - Set welcome channel
                .
                /welcome_clear - Remove the set welcome channel
                .
                /welcome_text {Optionally enter text - otherwise the default will be set} - Set welcome text
                .
                /goodbye - Displays this message
                .
                /goodbye_channel [#channel mention] - Set goodbye channel
                .
                /goodbye_clear - Remove the set goodbye channel
                .
                /goodbye_text {Optionally enter text - otherwise the default will be set} - Set goodbye text

                """
        goodbyehelp = disnake.Embed(
            title=":wave: Welcome & Goodbye Messages",
            description=f"{descwelcgood}",
        ).set_author(name="Help System")
        await inter.response.send_message(embed=goodbyehelp)

    @commands.slash_command(name="goodbye_channel", description="Set")
    async def goodbye_channel(
        self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel
    ):
        """
        Sets the channel where the goodbye message will be sent.

        Parameters:
        channel (disnake.TextChannel): The channel to set as the goodbye channel.
        """
        if not inter.author.guild_permissions.manage_channels:
            await inter.response.send_message(
                "You do not have enough permissions - You require **Manage Channels**",
                ephemeral=True,
            )
            return

        try:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(
                db.select_table("goodbye", "channel_id", "guild_id", inter.guild.id)
            )
            result = cursor.fetchone()
            if result is None:
                val = (inter.guild.id, channel.id)
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
                        inter.guild.id,
                    )
                )
            connect.commit()
            cursor.close()
            connect.close()
            await inter.response.send_message(
                f"Set the goodbye channel in {inter.guild} to {channel.mention}",
                ephemeral=True,
            )
        except Exception as e:
            await inter.response.send_message(
                f"Failed to set channel: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="goodbye_clear", description="Clear")
    async def goodbye_clear(self, inter: disnake.ApplicationCommandInteraction):
        """
        Removes the configured goodbye channel.
        """
        if not inter.author.guild_permissions.manage_channels:
            await inter.response.send_message(
                "You do not have enough permissions - You require **Manage Channels**.",
                ephemeral=True,
            )
            return

        try:
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(
                db.select_table("goodbye", "channel_id", "guild_id", inter.guild.id)
            )
            result = cursor.fetchone()
            if result is None:
                await inter.response.send_message(
                    "No goodbye channel is set for this server.", ephemeral=True
                )
            else:
                cursor.execute(db.delete_table("goodbye", "guild_id", inter.guild.id))
                await inter.response.send_message(
                    "Cleared the goodbye channel setting", ephemeral=True
                )
            connect.commit()
            cursor.close()
            connect.close()
        except Exception as e:
            await inter.response.send_message(
                f"Failed to remove goodbye channel setting: {str(e)}", ephemeral=True
            )

    @commands.slash_command(name="goodbye_text", description="Set")
    async def goodbye_text(
        self, inter: disnake.ApplicationCommandInteraction, content: str = None
    ):
        """
        Sets the text of the goodbye message.

        Parameters:
        content (str, optional): The custom goodbye message. If not provided, a default message will be set.
        """
        if not inter.author.guild_permissions.manage_channels:
            await inter.response.send_message(
                "You do not have enough permissions - You require **Manage Channels**.",
                ephemeral=True,
            )
            return

        try:
            if content is None:
                content = "A person left, who knows his/hers reasons for leaving but we will welcome them with open arms if they return "
                await inter.response.send_message(
                    "Setting default message", ephemeral=True
                )

            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(
                db.select_table("goodbye", "text", "guild_id", inter.guild.id)
            )
            res = cursor.fetchone()
            if res is None:
                val = (inter.guild.id, content)
                cursor.execute(db.insert_table("goodbye", "guild_id", "text"), val)
            else:
                val = (content, inter.guild.id)
                cursor.execute("UPDATE goodbye SET text = ? WHERE guild_id = ?", val)
            connect.commit()
            cursor.close()
            connect.close()
            await inter.response.send_message(
                "Set the goodbye message text", ephemeral=True
            )
        except Exception as e:
            await inter.response.send_message(
                f"Error setting goodbye text: {str(e)}", ephemeral=True
            )


def setup(bot):
    """

    :param bot: 

    """
    bot.add_cog(Goodbye(bot))
