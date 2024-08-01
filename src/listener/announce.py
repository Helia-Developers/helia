import asyncio
import os
import platform

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot
import psutil

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class Broadcast(commands.Cog):
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
                f"Discord.py version: {disnake.__version__}",
                f"Python version: {platform.python_version()}",
                f"Operating system: {platform.system()} {platform.release()}",
                f"CPU usage: {psutil.cpu_percent()}%",
                f"Memory usage: {psutil.virtual_memory().percent}%",
            ]
            
            # Add slash command description lengths
            debug_info.append("\nSlash Command Description Lengths:")
            for cog in inter.bot.cogs.values():
                for command in cog.get_slash_commands():
                    debug_info.append(f"Cog: {cog.__class__.__name__}, Command: {command.name}, Description Length: {len(command.description)}")
            
            # Join the debug info into a single string
            debug_message = "Debug Information:\n" + "\n".join(debug_info)
            
            # Split the message if it's too long
            if len(debug_message) > 2000:
                chunks = [debug_message[i:i+2000] for i in range(0, len(debug_message), 2000)]
                await inter.response.send_message(chunks[0])
                for chunk in chunks[1:]:
                    await inter.followup.send(chunk)
            else:
                await inter.response.send_message(debug_message)
        except Exception as e:
            await inter.response.send_message(
                f"An error occurred: {str(e)}", ephemeral=True
            )


def setup(bot):
    bot.add_cog(Broadcast(bot))
    print("Global announcements initialized")
