# -*- coding: utf-8 -*-
import math
import random
import re
from collections import Counter
from typing import Optional

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class Utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Utilities"

    @commands.slash_command(name="user", description="Shows user information")
    async def user(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        """
        Shows user information.

        Parameters:
        -----------
        member: The user to show information about. If not provided, shows information about the command user.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        member = member or inter.author

        embed = disnake.Embed(
            description=STRINGS["utilities"]["user_info"].format(
                member.id, member.created_at.strftime("%d.%m.%Y %H:%M"),
                member.joined_at.strftime("%d.%m.%Y %H:%M"), member.nick,
                member.status, member.activity, member.color),
            color=member.color,
        )
        embed.set_author(name=STRINGS["utilities"]["user_info_title"].format(member.name, member.discriminator))
        embed.set_thumbnail(url=member.avatar.url)

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="emoji", description="Shows emoji information")
    async def emoji(self, inter: disnake.ApplicationCommandInteraction, emoji: str):
        """
        Shows emoji information.

        Parameters:
        -----------
        emoji: The emoji to show information about.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        try:
            format = "png" if re.sub(r"[\<]", "", emoji.split(":")[0]) == "" else "gif"
            name = emoji.split(":")[1]
            id = re.sub(r"[\>]", "", emoji.split(r":")[2])

            embed = disnake.Embed(
                title=STRINGS["utilities"]["emoji_info_title"].format(name),
                color=0xEDA84E)
            embed.set_image(url=f"https://cdn.discordapp.com/emojis/{id}.{format}")
            embed.set_footer(text=STRINGS["utilities"]["emoji_info"].format(id))

            await inter.response.send_message(embed=embed)
        except IndexError:
            await inter.response.send_message("Invalid emoji format. Please use a custom emoji.", ephemeral=True)

    @commands.slash_command(name="channel", description="Shows channel information")
    async def channel(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.abc.GuildChannel):
        """
        Shows channel information.

        Parameters:
        -----------
        channel: The channel to show information about.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        channel_type = STRINGS["etc"]["channel_type"]["text"]
        if isinstance(channel, disnake.VoiceChannel):
            channel_type = STRINGS["etc"]["channel_type"]["voice"]
        elif isinstance(channel, disnake.TextChannel) and channel.is_news():
            channel_type = STRINGS["etc"]["channel_type"]["news"]

        is_nsfw = STRINGS["etc"]["other"]["yes"] if channel.is_nsfw() else STRINGS["etc"]["other"]["no"]

        embed = disnake.Embed(
            description=STRINGS["utilities"]["channel_info"].format(
                channel.id, channel_type, channel.created_at.strftime("%d.%m.%Y %H:%M"), is_nsfw),
            color=0xEDA84E,
        )
        embed.set_author(name=STRINGS["utilities"]["channel_info_title"].format(channel.name))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="avatar", description="Shows user's avatar")
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        """
        Shows user's avatar.

        Parameters:
        -----------
        member: The user whose avatar to show. If not provided, shows the command user's avatar.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        member = member or inter.author
        avatar = member.avatar.url

        embed = disnake.Embed(
            color=0xEDA84E,
            title=STRINGS["utilities"]["avatar_info_title"].format(member.name, member.discriminator),
            description=STRINGS["utilities"]["avatar_info"].format(member.avatar.key, avatar),
        )
        embed.set_image(url=avatar)

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="randint", description="Random number generator")
    async def randint(self, inter: disnake.ApplicationCommandInteraction, min_value: int, max_value: int):
        """
        Generates a random integer between min_value and max_value (inclusive).

        Parameters:
        -----------
        min_value: The minimum value for the random number.
        max_value: The maximum value for the random number.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if min_value > max_value:
            min_value, max_value = max_value, min_value

        result = random.randint(min_value, max_value)
        embed = disnake.Embed(
            title=STRINGS["generictext"]["randinttitle"],
            description=STRINGS["generictext"]["descgenermath"],
        )
        embed.add_field(name=STRINGS["generictext"]["numberone"], value=f"{min_value}", inline=True)
        embed.add_field(name=STRINGS["generictext"]["numbertwo"], value=f"{max_value}", inline=True)
        embed.add_field(name=STRINGS["generictext"]["result"], value=f"{result}", inline=False)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="sqrt", description="Calculate square root")
    async def sqrt(self, inter: disnake.ApplicationCommandInteraction, num: int):
        """
        Calculates the square root of a given number.

        Parameters:
        -----------
        num: The number to calculate the square root of.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if num < 0:
            embed = disnake.Embed(
                title=STRINGS["error"]["on_error_title"],
                description=STRINGS["error"]["localeerrortext"],
                color=0xFF0000,
            )
            embed.add_field(
                name=STRINGS["generictext"]["invalidvalue"],
                value=STRINGS["generictext"]["valmath"],
                inline=False,
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        result = math.sqrt(num)
        embed = disnake.Embed(
            title=STRINGS["generictext"]["sqsqrt"],
            description=STRINGS["generictext"]["math"],
        )
        embed.add_field(name=STRINGS["generictext"]["entered"], value=f"{num}", inline=False)
        embed.add_field(name=STRINGS["generictext"]["result"], value=f"{result}", inline=True)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="guild", description="Shows guild information")
    async def guild(self, inter: disnake.ApplicationCommandInteraction, guild_id: Optional[int] = None):
        """
        Shows guild information.

        Parameters:
        -----------
        guild_id: The ID of the guild to show information about. If not provided, shows information about the current guild.
        """
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if guild_id is not None and await self.bot.is_owner(inter.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await inter.response.send_message("Invalid Guild ID given.", ephemeral=True)
        else:
            guild = inter.guild

        if not guild.chunked:
            await guild.chunk(cache=True)

        # Calculate channel statistics
        channel_stats = Counter(type(c) for c in guild.channels)
        channel_info = [
            f":bookmark_tabs: Text Channels: {channel_stats[disnake.TextChannel]}",
            f":speaker: Voice Channels: {channel_stats[disnake.VoiceChannel]}",
            f":newspaper: News Channels: {channel_stats[disnake.TextChannel]}"
        ]

        # Create embed
        e = disnake.Embed(title=guild.name, description=f"**ID**: {guild.id}\n**Owner**: {guild.owner}")
        e.set_thumbnail(url=guild.icon.url if guild.icon else "https://i.imgur.com/SAigvsR.png")

        # Add fields
        e.add_field(name="Channels", value="\n".join(channel_info), inline=False)
        e.add_field(name="Members", value=f"Total: {guild.member_count}", inline=True)
        e.add_field(name="Roles", value=f"{len(guild.roles)} roles", inline=True)

        # Emoji statistics
        emoji_stats = Counter(animated=sum(e.animated for e in guild.emojis))
        emoji_stats['regular'] = len(guild.emojis) - emoji_stats['animated']
        emoji_info = (
            f"Regular: {emoji_stats['regular']}/{guild.emoji_limit}\n"
            f"Animated: {emoji_stats['animated']}/{guild.emoji_limit}\n"
            f"Total Emoji: {len(guild.emojis)}/{guild.emoji_limit*2}"
        )
        e.add_field(name="Emoji", value=emoji_info, inline=False)

        await inter.response.send_message(embed=e)


def setup(bot: Bot) -> None:
    bot.add_cog(Utilities(bot))
    Logger.cog_loaded(bot.get_cog("Utilities").name)