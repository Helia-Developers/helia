import asyncio
from typing import NoReturn

import disnake
from disnake import Member, User
from disnake.ext import commands
from disnake.ext.commands import Bot, Context, Greedy
from termcolor import cprint

from listener.utils import Config, Logger, Settings, Strings, Utils

# from disnake_components import Button, ButtonStyle, disnakeComponents

CONFIG = Config()


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Moderation"

    @commands.command(slash_interaction=True, message_command=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(
        self, ctx: Context, member: Member, *, reason: str = "N/A"
    ) -> NoReturn:
        """


        A command to ban a specified user.

        Arguments:
        -----------
        - `member` - user
        - `reason` - ban reason

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        # select_components = [[
        # Button(style=ButtonStyle.green, label="✓"),
        # Button(style=ButtonStyle.red, label="X"),
        # ]]
        # done_components = [[
        # Button(style=ButtonStyle.grey, label="·", disabled=True),
        # ]]

        # embedconfirm = disnake.Embed(
        # title="Ban Command",
        # description="```Do you want to ban this member?```",
        # )
        # await ctx.send(embed=embedconfirm, components=select_components)
        # response = await self.bot.wait_for(
        # "button_click", check=lambda message: message.author == ctx.author)
        # try:
        # if response.component.label == "✓":
        # await response.respond(
        # type=7,
        # embed=disnake.Embed(
        # title="Action confirmed",
        # description=f"Banning {member} for {reason}",
        # color=0xFF8000,
        # ),
        # components=done_components,
        # )
        if not member.bot:
            embed = Utils.error_embed(
                STRINGS["moderation"]["dm_kick"].format(ctx.guild, reason)
            )
            await member.send(embed=embed)
        await asyncio.sleep(5)
        await member.ban(reason=reason)
        cprint(
            f"""
        ║============================================================║
        ║--------Succesfully banned {member} in {ctx.guild.name}-------║
        ║============================================================║
        """
        )

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(self, ctx, *, member) -> NoReturn:
        """


        A command to unban a specified user.

        Arguments:
        -----------
        - `member` - user tag. Example: `name#1234`

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        # select_components = [[
        # Button(style=ButtonStyle.green, label="✓"),
        # Button(style=ButtonStyle.red, label="X"),
        # ]]
        # done_components = [[
        # Button(style=ButtonStyle.grey, label="·", disabled=True),
        # ]]

        # embedconfirm = disnake.Embed(
        # title="Unban Command",
        # description="```Do you want to unban this member?```",
        # )
        # await ctx.send(embed=embedconfirm, components=select_components)
        # response = await self.bot.wait_for(
        # "button_click", check=lambda message: message.author == ctx.author)

        if "#" in ctx.message.content:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                member_name, member_discriminator = member.split("#")
                user = ban_entry.user
                if (user.name, user.discriminator) == (
                    member_name,
                    member_discriminator,
                ):
                    await ctx.guild.unban(user)
                    await ctx.send(
                        embed=disnake.Embed(
                            title="Action confirmed",
                            description=f"Unbanned {user}",
                            color=0xFF8000,
                        ),
                    )
            cprint(
                f"""
             ║============================================================║
             ║------Succesfully unbanned {member} in {ctx.guild.name}-------║
             ║============================================================║
            """
            )
            return
        elif member is int:
            member = await self.client.fetch_user(int(member))
            await ctx.guild.unban(member)
            await ctx.send(
                embed=disnake.Embed(
                    title="Action confirmed",
                    description=f"Unbanned {user}",
                    color=0xFF8000,
                ),
            )
            cprint(
                f"""
             ║============================================================║
             ║------Succesfully unbanned {member} in {ctx.guild.name}-------║
             ║============================================================║
            """
            )
        # else:
        # await response.respond(
        # type=7,
        # embed=disnake.Embed(
        # title="Action Aborted",
        # description="The action was aborted by clicking the no button",
        # color=0xDD2E44,
        # ),
        # components=done_components,
        # )

        await ctx.message.add_reaction(CONFIG["no_emoji"])
        embed = Utils.error_embed(STRINGS["error"]["user_not_found"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def multiban(
        self, ctx: Context, members: Greedy[Member], *, reason: str = "N/A"
    ) -> NoReturn:
        """


        A command to ban multiple users.

        Arguments:
        -----------
        - `member` - user
        - `reason` - ban reason

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        not_banned_members = []

        for member in members:
            try:
                await member.ban(reason=reason)
                await ctx.send("Members banned")

            except disnake.Forbidden:
                not_banned_members.append(member.mention)

            else:
                try:
                    embed = Utils.error_embed(
                        STRINGS["moderation"]["dm_ban"].format(ctx.guild.name, reason)
                    )
                    await member.send(embed=embed)
                except:
                    pass

        if not not_banned_members:
            await ctx.message.add_reaction(CONFIG["yes_emoji"])
        else:
            await ctx.message.add_reaction(CONFIG["warn_emoji"])
            msg = await ctx.send(
                Utils.warn_embed(
                    STRINGS["moderation"]["on_not_full_multiban"].format(
                        ", ".join(not_banned_members)
                    )
                )
            )
            await asyncio.sleep(30)
            await msg.delete()

    @commands.command()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(
        self, ctx: Context, member: Member, *, reason: str = "N/A"
    ) -> NoReturn:
        """


        A command to kick a specified user.

        Arguments:
        -----------
        - `member` - user
        - `reason` - kick reason

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        select_components = [
            [
                Button(style=ButtonStyle.green, label="✓"),
                Button(style=ButtonStyle.red, label="X"),
            ]
        ]
        done_components = [
            [
                Button(style=ButtonStyle.grey, label="·", disabled=True),
            ]
        ]

        embedconfirm = disnake.Embed(
            title="Kick Command",
            description="```Do you want to kick this member?```",
        )
        await ctx.send(embed=embedconfirm, components=select_components)
        response = await self.bot.wait_for(
            "button_click", check=lambda message: message.author == ctx.author
        )
        if response.component.label == "✓":
            await response.respond(
                type=7,
                embed=disnake.Embed(
                    title="Action Completed",
                    description=f"Kicked {member} for {reason}",
                    color=0xDD2E44,
                ),
                components=done_components,
            )
            if not member.bot:
                embed = Utils.error_embed(
                    STRINGS["moderation"]["dm_kick"].format(ctx.guild, reason)
                )
                await member.send(embed=embed)
            await asyncio.sleep(5)
            await member.kick()
            await ctx.message.add_reaction(CONFIG["yes_emoji"])
        else:
            await response.respond(
                type=7,
                embed=disnake.Embed(
                    title="Action Aborted",
                    description="The action was aborted by clicking the no button",
                    color=0xDD2E44,
                ),
                components=done_components,
            )
            return

    @commands.command(aliases=["clear"])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx: Context, number: int) -> NoReturn:
        """


        Deletes a specified number of messages in the current channel.

        Arguments:
        -----------
        - `number` - The number of messages to be deleted.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        # select_components = [[
        # Button(style=ButtonStyle.green, label="✓"),
        # Button(style=ButtonStyle.red, label="X"),
        # ]]
        # done_components = [[
        # Button(style=ButtonStyle.grey, label="·", disabled=True),
        # ]]

        # embedconfirm = disnake.Embed(
        # title="Clear Command",
        # description=f"```Do you want to remove {number} messages?```",
        # )
        # await ctx.send(embed=embedconfirm, components=select_components)
        # response = await self.bot.wait_for(
        # "button_click", check=lambda message: message.author == ctx.author)

        await ctx.send(
            embed=disnake.Embed(
                title="Action Completed",
                description=f"Purging {number} messages",
                color=0xDD2E44,
            )
        )
        await asyncio.sleep(10)
        deleted = await ctx.channel.purge(limit=number + 1)

        # else:
        # await response.respond(
        # type=7,
        # embed=disnake.Embed(
        # title="Action Aborted",
        # description="The action was aborted by clicking the no button",
        # color=0xDD2E44,
        # ),
        # components=done_components,
        # )
        # return

    @commands.command(aliases=["setnick, setname"])
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setname(self, ctx: Context, member: Member, *, name: str) -> NoReturn:
        """


        Set a nickname for the specified user.

        Arguments:
        -----------
        - `member` - user.
        - `name` - Nickname to set

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if len(name) > 32:
            embed = Utils.error_embed(STRINGS["error"]["too_long_name"])
            await ctx.send(embed=embed)
        elif (
            ctx.message.author.guild_permissions.manage_nicknames
            or member == ctx.message.author
        ):
            await member.edit(nick=name)
            await ctx.message.add_reaction(CONFIG["yes_emoji"])
        else:
            embed = Utils.error_embed(STRINGS["error"]["missing_perms"])
            await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mute(
        self, ctx: Context, member: Member, *, reason: str = "N/A"
    ) -> NoReturn:
        """


        Makes a specified user muted which basically means they cannot talk.

        Arguments:
        -----------
        - `member` - user.
        - `reason` - Reason to mute the person

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        mute_role_id = await s.get_field("mute_role_id")

        if (
            mute_role_id is None
            or disnake.utils.get(ctx.guild.roles, id=mute_role_id) is None
        ):
            embed = Utils.done_embed(STRINGS["moderation"]["on_mute_role_create"])
            await ctx.send(embed=embed)
            mute_role = await ctx.guild.create_role(name="Muted")

            await s.set_field("mute_role_id", mute_role.id)
            mute_role_id = await s.get_field("mute_role_id")

        else:
            mute_role = disnake.utils.get(ctx.guild.roles, id=mute_role_id)

            for user_role in member.roles:
                if user_role == mute_role:
                    embed = Utils.error_embed(STRINGS["error"]["already_muted"])
                    await ctx.send(embed=embed)
                    return

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(
                mute_role, read_messages=True, send_messages=False, speak=False
            )

        await member.add_roles(mute_role)
        await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(
        self, ctx: Context, member: Member, *, reason: str = "N/A"
    ) -> NoReturn:
        """


        Unmutes a specified user which allows them to talk again.

        Arguments:
        -----------
        - `member` - user.
        - `reason` - Reason to unmute the person

        """
        mute_role = disnake.utils.get(
            ctx.guild.roles, id=Utils.get_mute_role(None, ctx.message)
        )
        if mute_role is None:
            # FIXME
            await ctx.send("нету роли мута ок да\n\n\nок")
        else:
            await member.remove_roles(mute_role)
            await ctx.message.add_reaction(CONFIG["yes_emoji"])

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    # `RoleConverter` will automatically convert it to a `disnake.Role` instance
    async def lockdownrole(self, ctx, role: disnake.Role):
        """


        Disables writing permissions for a specified role in server.

        Arguments:
        -----------
        - `role` - Role for which to disallow writing in server.


        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["lockdowntitleone"],
            description=STRINGS["moderation"]["lockdowndescone"],
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def unlockrole(self, ctx, role: disnake.Role):
        """


        Allows  writing permissions for a specfied role in server.

        Arguments:
        -----------
        - `role` - Role for which to disallow writing in server.


        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=True)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["lockdownliftedtitleone"],
            description=STRINGS["moderation"]["lockdownlifteddescone"],
            color=0x6E8F5D,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def lockdown(self, ctx):
        """


        Disables writing permissions for everyone in the server.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["lockdowntitleone"],
            description=STRINGS["moderation"]["lockdowndescone"],
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def unlock(self, ctx):
        """


        Allows writing permissions for everyone in the server.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["lockdownliftedtitleone"],
            description=STRINGS["moderation"]["lockdownlifteddescone"],
            color=0x6E8F5D,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def channellock(self, ctx):
        """


        Disables writing permissions in current channel.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["channellockdowntitle"],
            description=STRINGS["moderation"]["channellockdowndesc"],
            color=0x000000,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def channelunlock(self, ctx):
        """

        Allows writing permissions in current channel.

        """
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = disnake.Embed(
            title=STRINGS["moderation"]["channellockdownliftedtitle"],
            description=STRINGS["moderation"]["channellockdownlifteddesc"],
            color=0x6E8F5D,
        )
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Moderation(bot))
    Logger.cog_loaded(bot.get_cog("Moderation").name)
