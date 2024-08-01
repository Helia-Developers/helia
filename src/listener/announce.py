import asyncio
import os
import platform

import disnake
import psutil
from disnake.ext import commands
from disnake.ext.commands import Bot

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class Broadcast(commands.Cog):
    """ """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="announce",
        description="Announce",
    )
    @commands.is_owner()
    async def announce(
        self, inter: disnake.ApplicationCommandInteraction, content: str
    ):
        """
        Send a global announcement to all servers.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object.
        content: str
            The content of the announcement.
        """
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            prefix = await s.get_field("prefix", CONFIG["default_prefix"])
            STRINGS = Strings(lang)
            announcement = disnake.Embed(
                title=STRINGS["general"]["announcestitle"],
                description=STRINGS["general"]["announcesdesc"],
                color=0x3B88C3,
            )
            author_name = f"{inter.author}"
            announcement.set_author(name=author_name, icon_url=inter.author.avatar.url)
            announcement.add_field(
                name=STRINGS["general"]["announcesfieldtitle"],
                value=f"{inter.guild.name}",
                inline=False,
            )
            announcement.add_field(
                name=STRINGS["general"]["announcesfielddesc"],
                value=content,
                inline=True,
            )
            announcement.set_footer(
                text=STRINGS["general"]["announcesfooter"],
                icon_url=inter.guild.icon.url,
            )
            sent_counter = 0
            text_channel_list = []
            embed = disnake.Embed(
                title=STRINGS["general"]["announcestitle"],
                description=STRINGS["general"]["announceaway"],
            )
            embed.set_author(name=self.bot.user.name)
            await inter.response.send_message(embed=embed)
            for guild in self.bot.guilds:
                try:
                    await guild.text_channels[0].send(embed=announcement)
                    sent_counter += 1
                except disnake.Forbidden:
                    continue
                except disnake.NotFound:
                    continue
                except Exception as e:
                    print(f"Error sending announcement to guild {guild.id}: {str(e)}")

            await inter.followup.send(f"Announcement sent to {sent_counter} servers.")
        except Exception as e:
            await inter.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

    """
    Get debug information about the bot.
    
    Parameters:
    -----------
    inter: disnake.ApplicationCommandInteraction
        The interaction object.
    """

    @commands.slash_command(
        name="debug",
        description="Debug",
    )
    @commands.is_owner()
    async def debug(self, inter: disnake.ApplicationCommandInteraction):
        """
        Get debug information about the bot.

        Parameters:
        -----------
        inter: disnake.ApplicationCommandInteraction
            The interaction object.
        """
        try:
            voice_states = inter.bot.voice_clients
            guilds = inter.bot.guilds
            total_members = sum(guild.member_count for guild in guilds)

            debug_info = [
                f"Voice channels: {len(voice_states)}",
                f"Servers: {len(guilds)}",
                f"Total members: {total_members}",
                f"Latency: {round(inter.bot.latency * 1000)}ms",
                f"Disnake.py version: {disnake.__version__}",
                f"Python version: {platform.python_version()}",
                f"Operating system: {platform.system()} {platform.release()}",
                f"CPU usage: {psutil.cpu_percent()}%",
                f"Memory usage: {psutil.virtual_memory().percent}%",
            ]

            # Add bot permissions
            bot_permissions = inter.guild.me.guild_permissions
            permission_info = ["Bot Permissions:"]
            for permission, value in bot_permissions:
                if value:
                    permission_info.append(f"- {permission}")

            # Add slash command description lengths
            command_info = ["Slash Command Description Lengths:"]
            for cog in inter.bot.cogs.values():
                for command in cog.get_slash_commands():
                    command_info.append(
                        f"Cog: {cog.__class__.__name__}, Command: {command.name}, Description Length: {len(command.description)}"
                    )

            # Create the embed
            embed = disnake.Embed(title="Debug Information", color=disnake.Color.blue())

            # Add main debug info to embed
            embed.add_field(
                name="General Info", value=f"\n{chr(10).join(debug_info)}", inline=False
            )

            # Add permissions to embed
            embed.add_field(
                name="Permissions",
                value=f"\n{chr(10).join(permission_info[:25])}",
                inline=False,
            )

            # Add command info to embed
            command_chunks = [
                command_info[i : i + 20] for i in range(0, len(command_info), 20)
            ]
            for i, chunk in enumerate(command_chunks):
                chunk_value = "\n".join(chunk)
                if len(chunk_value) > 1024:
                    chunk_value = chunk_value[:1021] + "..."
                embed.add_field(
                    name=f"Command Info (Part {i+1})", value=chunk_value, inline=False
                )

            # Check if the embed content is too long
            if len(embed) > 2000:
                # Split the embed into multiple messages
                await inter.response.send_message(
                    "Debug information (Part 1):", embed=embed
                )

                # Create additional embeds for the remaining fields
                additional_embeds = []
                current_embed = disnake.Embed(
                    title="Debug Information (Continued)", color=disnake.Color.blue()
                )
                for field in embed.fields[len(embed.fields) // 2 :]:
                    if len(current_embed) + len(field.value) > 1000:
                        additional_embeds.append(current_embed)
                        current_embed = disnake.Embed(
                            title="Debug Information (Continued)",
                            color=disnake.Color.blue(),
                        )
                    current_embed.add_field(
                        name=field.name, value=field.value, inline=field.inline
                    )

                if len(current_embed.fields) > 0:
                    additional_embeds.append(current_embed)

                # Send additional embeds
                for i, embed in enumerate(additional_embeds):
                    await inter.followup.send(
                        f"Debug information (Part {i+2}):", embed=embed
                    )
            else:
                await inter.response.send_message(embed=embed)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )


def setup(bot):
    """

    :param bot: 

    """
    bot.add_cog(Broadcast(bot))
    print("Global announcements initialized")
