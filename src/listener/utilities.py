"""
Provides a set of utility commands for the Discord bot.

The `Utilities` class is a Cog that adds several utility commands to the bot, including:

- `user`: Displays information about a user, such as their ID, username, join date, and status.
- `emoji`: Displays information about an emoji, including its name and a preview of the emoji.
- `channel`: Displays information about a channel, including its type, creation date, and whether it is NSFW.
- `avatar`: Displays a user's avatar image.
- `randint`: Generates a random integer between two given numbers.
- `sqrt`: Calculates the square root of a given number.
- `guild`: Displays information about the current guild, including the number of channels, members, and roles.

These commands can be used both as slash commands and message commands.
"""
# -*- coding: utf-8 -*-
import math
import random
import re
from collections import Counter, OrderedDict, deque
from typing import NoReturn

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()


class Utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Utilities"

    @commands.command(slash_command=True, message_command=True)
    async def user(self,
                   ctx: Context,
                   member: disnake.Member = None) -> NoReturn:
        """Shows user information.

        Attributes:
        -----------
        - `member` - user

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if member is None:
            member = ctx.message.author

        id = str(member.id)
        name = member.name
        tag = member.discriminator
        username = member.nick
        joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M")
        created_at = member.created_at.strftime("%d.%m.%Y %H:%M")
        stat = member.status
        activ = member.activity
        color = member.color
        avatar = member.avatar.url

        embed = disnake.Embed(
            description=STRINGS["utilities"]["user_info"].format(
                id, created_at, joined_at, username, stat, activ, color),
            color=color,
        )
        embed.set_author(
            name=STRINGS["utilities"]["user_info_title"].format(name, tag))
        embed.set_thumbnail(url=avatar)

        await ctx.send(embed=embed)

    @commands.command(slash_command=True, message_command=True)
    async def emoji(self, ctx: Context, emoji: str) -> NoReturn:
        """Shows emoji information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        format = r"png" if re.sub(r"[\<]", r"",
                                  emoji.split(":")[0]) == "" else "gif"
        name = emoji.split(":")[1]
        id = re.sub(r"[\>]", r"", emoji.split(r":")[2])

        embed = disnake.Embed(
            title=STRINGS["utilities"]["emoji_info_title"].format(name),
            color=0xEDA84E)
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{id}.{format}")
        embed.set_footer(text=STRINGS["utilities"]["emoji_info"].format(id))

        await ctx.send(embed=embed)

    @commands.command(slash_command=True, message_command=True)
    async def channel(self, ctx: Context, channel: str) -> NoReturn:
        """Shows channel information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if re.search(r"[@&\:]", channel) is None:

            channel = disnake.utils.get(ctx.guild.channels,
                                        id=int(re.sub("[<#>]", "", channel)))

            if (channel.type
                    == disnake.ChannelType.text) or channel.type not in [
                        disnake.ChannelType.voice,
                        disnake.ChannelType.news,
            ]:
                type = STRINGS["etc"]["channel_type"]["text"]
            elif channel.type == disnake.ChannelType.voice:
                type = STRINGS["etc"]["channel_type"]["voice"]
            else:
                type = STRINGS["etc"]["channel_type"]["news"]
            if channel.nsfw:
                is_nsfw = STRINGS["etc"]["other"]["yes"]
            else:
                is_nsfw = STRINGS["etc"]["other"]["no"]

            name = channel.name
            id = channel.id
            created_at = channel.created_at.strftime("%d.%m.%Y %H:%M")

            embed = disnake.Embed(
                description=STRINGS["utilities"]["channel_info"].format(
                    id, type, created_at, is_nsfw),
                color=0xEDA84E,
            )
            embed.set_author(
                name=STRINGS["utilities"]["channel_info_title"].format(name))
            await ctx.send(embed=embed)

        else:
            await ctx.send("чел, это не канал, ты что-то попутал")

    @commands.command(slash_command=True, message_command=True)
    async def avatar(self,
                     ctx: Context,
                     member: disnake.Member = None) -> NoReturn:
        """Shows user's avatar.

        Attributes:
        -----------
        - `member` - user

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if member is None:
            member = ctx.message.author
        name = member.name
        tag = member.discriminator
        avatar = member.avatar.url
        hash = member.avatar

        embed = disnake.Embed(
            color=0xEDA84E,
            title=STRINGS["utilities"]["avatar_info_title"].format(name, tag),
            description=STRINGS["utilities"]["avatar_info"].format(
                hash, avatar),
        )
        embed.set_image(url=avatar)

        await ctx.send(embed=embed)

    @commands.command(
        slash_command=True,
        message_command=True,
        description="Random number generator",
    )
    async def randint(self, ctx: Context, stc1: int, stc2: int):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        result = random.randint(stc1, stc2)
        embed = disnake.Embed(
            title=STRINGS["generictext"]["randinttitle"],
            description=STRINGS["generictext"]["descgenermath"],
        )
        embed.add_field(name=STRINGS["generictext"]["numberone"],
                        value=f"```{stc1}```",
                        inline=True)
        embed.add_field(name=STRINGS["generictext"]["numbertwo"],
                        value=f"```{stc2}```",
                        inline=True)
        embed.add_field(name=STRINGS["generictext"]["result"],
                        value=f"```{result}```",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(slash_command=True,
                      message_command=True,
                      description="Count square root")
    async def sqrt(self, ctx: Context, num: int):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        if num > 5000 or num < 0:
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
            await ctx.send(embed=embed)
            return
        else:
            result = math.sqrt(num)
            embed = disnake.Embed(
                title=STRINGS["generictext"]["sqsqrt"],
                description=STRINGS["generictext"]["math"],
            )
            embed.add_field(
                name=STRINGS["generictext"]["entered"],
                value=f"```{num}```",
                inline=False,
            )
            embed.add_field(
                name=STRINGS["generictext"]["result"],
                value=f"```{result}```",
                inline=True,
            )
            await ctx.send(embed=embed)

    @commands.command(slash_command=True,
                      message_command=True,
                      aliases=["server"])
    async def guild(self, ctx, *, guild_id: int = None) -> NoReturn:
        """Shows guild information."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send("Invalid Guild ID given.")
        else:
            guild = ctx.guild

        roles = [role.name.replace("@", "@\u200b") for role in guild.roles]

        if not guild.chunked:
            async with ctx.typing():
                await guild.chunk(cache=True)

        # figure out what channels are 'secret'
        everyone = guild.default_role
        everyone_perms = everyone.permissions.value
        secret = Counter()
        totals = Counter()
        for channel in guild.channels:
            allow, deny = channel.overwrites_for(everyone).pair()
            perms = disnake.Permissions((everyone_perms & ~deny.value)
                                        | allow.value)
            channel_type = type(channel)
            totals[channel_type] += 1
            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel,
                            disnake.VoiceChannel) and (not perms.connect
                                                       or not perms.speak):
                secret[channel_type] += 1

        e = disnake.Embed()
        e.title = guild.name
        e.description = f"**ID**: {guild.id}\n**Owner**: {guild.owner}"
        if guild.icon:
            e.set_thumbnail(url=f"{guild.icon.url}")
        else:
            e.set_thumbnail(
                url="https://i.imgur.com/SAigvsR.png")

        channel_info = []
        key_to_emoji = {
            disnake.TextChannel: ":bookmark_tabs:",
            disnake.VoiceChannel: ":speaker:",
        }
        for key, total in totals.items():
            secrets = secret[key]
            try:
                emoji = key_to_emoji[key]
            except KeyError:
                continue

            if secrets:
                channel_info.append(f"{emoji} {total} ({secrets} locked)")
            else:
                channel_info.append(f"{emoji} {total}")

        features = set(guild.features)
        all_features = {
            "PARTNERED": "Partnered",
            "VERIFIED": "Verified",
            "DISCOVERABLE": "Server Discovery",
            "COMMUNITY": "Community Server",
            "FEATURABLE": "Featured",
            "WELCOME_SCREEN_ENABLED": "Welcome Screen",
            "INVITE_SPLASH": "Invite Splash",
            "VIP_REGIONS": "VIP Voice Servers",
            "VANITY_URL": "Vanity Invite",
            "COMMERCE": "Commerce",
            "LURKABLE": "Lurkable",
            "NEWS": "News Channels",
            "ANIMATED_ICON": "Animated Icon",
            "BANNER": "Banner",
        }

        info = [
            f'{CONFIG["yes_emoji"]}: {label}'
            for feature, label in all_features.items() if feature in features
        ]

        if info:
            e.add_field(name="Features", value="\n".join(info))

        e.add_field(name="Channels", value="\n".join(channel_info))

        # if guild.premium_tier != 0:
        # boosts = f'Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts'
        # last_boost = max(guild.members, key=lambda m: m.premium_since or guild.created_at)
        # if last_boost.premium_since is not None:
        # boosts = f'{boosts}\nLast Boost: {last_boost} ({time.format_relative(last_boost.premium_since)})'
        # e.add_field(name='Boosts', value=boosts, inline=False)

        bots = sum(m.bot for m in guild.members)
        fmt = f"Total: {guild.member_count} "

        e.add_field(name="Members", value=fmt, inline=True)
        e.add_field(
            name="Roles",
            value=", ".join(roles)
            if len(roles) < 10 else f"{len(roles)} roles",
        )

        emoji_stats = Counter()
        for emoji in guild.emojis:
            if emoji.animated:
                emoji_stats["animated"] += 1
                emoji_stats["animated_disabled"] += not emoji.available
            else:
                emoji_stats["regular"] += 1
                emoji_stats["disabled"] += not emoji.available

        fmt = (f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit}\n'
               f'Animated: {emoji_stats["animated"]}/{guild.emoji_limit}\n')
        if emoji_stats["disabled"] or emoji_stats["animated_disabled"]:
            fmt = f'{fmt}Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f"{fmt}Total Emoji: {len(guild.emojis)}/{guild.emoji_limit*2}"
        e.add_field(name="Emoji", value=fmt, inline=True)
        # e.set_footer(text='Created').timestamp = guild.created_at
        await ctx.send(embed=e)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Utilities(bot))
    Logger.cog_loaded(bot.get_cog("Utilities").name)
