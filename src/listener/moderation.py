import asyncio
from typing import NoReturn

import disnake
from disnake import Member, User
from disnake.ext import commands
from disnake.ext.commands import Bot, Context, Greedy
from disnake.ext.commands.params import Param
from termcolor import cprint

from listener.utils import Config, Logger, Settings, Strings, Utils

CONFIG = Config()


class Moderation(commands.Cog, name="Moderation"):
    """ """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = "Moderation"

    @commands.slash_command(description="Ban member")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: Member = Param(description="User to ban"),
        reason: str = Param(description="Ban reason", default="N/A"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        try:
            if not member.bot:
                embed = Utils.error_embed(
                    STRINGS["moderation"]["dm_kick"].format(inter.guild, reason)
                )
                await member.send(embed=embed)
            await asyncio.sleep(5)
            await member.ban(reason=reason)
            cprint(
                f"""
            ║============================================================║
            ║--------Succesfully banned {member} in {inter.guild.name}-------║
            ║============================================================║
            """
            )
            await inter.edit_original_message(
                embed=disnake.Embed(
                    title="Action done",
                    description=f"Banned {member}",
                    color=0xFF8000,
                ),
            )
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )

    @commands.slash_command(description="Unban member")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: str = Param(description="User to unban"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        try:
            if "#" in member:
                banned_users = await inter.guild.bans()
                for ban_entry in banned_users:
                    member_name, member_discriminator = member.split("#")
                    user = ban_entry.user
                    if (user.name, user.discriminator) == (
                        member_name,
                        member_discriminator,
                    ):
                        await inter.guild.unban(user)
                        await inter.edit_original_message(
                            embed=disnake.Embed(
                                title="Action confirmed",
                                description=f"Unbanned {user}",
                                color=0xFF8000,
                            ),
                        )
                        return
            elif member.isdigit():
                user = await self.bot.fetch_user(int(member))
                await inter.guild.unban(user)
                await inter.edit_original_message(
                    embed=disnake.Embed(
                        title="Action confirmed",
                        description=f"Unbanned {user}",
                        color=0xFF8000,
                    ),
                )
                return

            embed = Utils.error_embed(STRINGS["error"]["user_not_found"])
            await inter.edit_original_message(embed=embed)
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )

    @commands.slash_command(description="Ban multiple")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def multiban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        members: str = Param(description="Users to ban (comma-separated)"),
        reason: str = Param(description="Ban reason", default="N/A"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        not_banned_members = []

        member_list = [member.strip() for member in members.split(",")]
        for member_id in member_list:
            try:
                member = await inter.guild.fetch_member(int(member_id))
                await member.ban(reason=reason)
                try:
                    embed = Utils.error_embed(
                        STRINGS["moderation"]["dm_ban"].format(inter.guild.name, reason)
                    )
                    await member.send(embed=embed)
                except disnake.HTTPException:
                    pass
            except disnake.Forbidden:
                not_banned_members.append(f"<@{member_id}>")
            except disnake.HTTPException:
                not_banned_members.append(f"<@{member_id}>")

        if not not_banned_members:
            await inter.edit_original_message(content="Members banned")
        else:
            await inter.edit_original_message(
                embed=Utils.warn_embed(
                    STRINGS["moderation"]["on_not_full_multiban"].format(
                        ", ".join(not_banned_members)
                    )
                )
            )

    @commands.slash_command(description="Kick member")
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: Member = Param(description="User to kick"),
        reason: str = Param(description="Kick reason", default="N/A"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        try:
            if not member.bot:
                embed = Utils.error_embed(
                    STRINGS["moderation"]["dm_kick"].format(inter.guild, reason)
                )
                await member.send(embed=embed)
            await asyncio.sleep(5)
            await member.kick(reason=reason)
            await inter.edit_original_message(
                embed=disnake.Embed(
                    title="Action Completed",
                    description=f"Kicked {member} for {reason}",
                    color=0xDD2E44,
                ),
            )
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )

    @commands.slash_command(description="Purge messages")
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(
        self,
        inter: disnake.ApplicationCommandInteraction,
        number: int = Param(description="Number of messages"),
    ) -> NoReturn:
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        await inter.response.defer()

        try:
            deleted = await inter.channel.purge(limit=number)
            await inter.edit_original_message(
                embed=disnake.Embed(
                    title="Action Completed",
                    description=f"Purged {len(deleted)} messages",
                    color=0xDD2E44,
                )
            )
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )

    @commands.slash_command(description="Set nickname")
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setname(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: Member = Param(description="User"),
        name: str = Param(description="New nickname"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if len(name) > 32:
            embed = Utils.error_embed(STRINGS["error"]["too_long_name"])
            await inter.edit_original_message(embed=embed)
        elif inter.author.guild_permissions.manage_nicknames or member == inter.author:
            try:
                await member.edit(nick=name)
                await inter.edit_original_message(content="Nickname changed")
            except disnake.Forbidden:
                await inter.edit_original_message(
                    embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
                )
            except disnake.HTTPException as e:
                await inter.edit_original_message(
                    embed=Utils.error_embed(f"An error occurred: {str(e)}")
                )
        else:
            embed = Utils.error_embed(STRINGS["error"]["missing_perms"])
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(description="Mute member")
    @commands.bot_has_permissions(moderate_members=True)
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: Member = Param(description="User to mute"),
        duration: int = Param(description="Duration in minutes"),
        reason: str = Param(description="Mute reason", default="N/A"),
    ) -> NoReturn:
        await inter.response.defer()
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        if member.is_timed_out():
            embed = Utils.error_embed(STRINGS["error"]["already_muted"])
            await inter.edit_original_message(embed=embed)
            return

        try:
            await member.timeout(duration=duration * 60, reason=reason)
            await inter.edit_original_message(
                content=f"{member} has been muted for {duration} minutes."
            )
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )

    @commands.slash_command(description="Unmute member")
    @commands.bot_has_permissions(moderate_members=True)
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: Member = Param(description="User to unmute"),
        reason: str = Param(description="Unmute reason", default="N/A"),
    ) -> NoReturn:
        s = await Settings(inter.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)

        await inter.response.defer()

        if not member.is_timed_out():
            await inter.edit_original_message(content="This user is not muted.")
            return

        try:
            await member.timeout(duration=0, reason=reason)
            await inter.edit_original_message(content=f"{member} has been unmuted.")
        except disnake.Forbidden:
            await inter.edit_original_message(
                embed=Utils.error_embed(STRINGS["error"]["missing_perms"])
            )
        except disnake.HTTPException as e:
            await inter.edit_original_message(
                embed=Utils.error_embed(f"An error occurred: {str(e)}")
            )
    @commands.slash_command(name="lockdown", description="Server lockdown commands")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def lockdowns(self, inter: disnake.ApplicationCommandInteraction, subcommand: str = commands.Param(choices=["lockdownrole", "unlockrole", "lockdown", "unlock", "channellock", "channelunlock"])):
        if subcommand == "lockdownrole":
            await self.lockdownrole(inter)
        elif subcommand == "unlockrole":
            await self.unlockrole(inter)
        elif subcommand == "lockdown":
            await self.lockdown(inter)
        elif subcommand == "unlock":
            await self.unlock(inter)
        elif subcommand == "channellock":
            await self.channellock(inter)
        elif subcommand == "channelunlock":
            await self.channelunlock(inter)
        else:
            await inter.response.send_message("Invalid subcommand.", ephemeral=True)

    @commands.has_permissions(manage_roles=True, manage_channels=True)
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def lockdownrole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = Param(description="Role to lockdown"),
    ):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for channel in inter.guild.channels:
                await channel.set_permissions(role, send_messages=False)
            embed = disnake.Embed(
                title=STRINGS["moderation"]["lockdowntitleone"],
                description=STRINGS["moderation"]["lockdowndescone"],
            )
            await inter.edit_original_message(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while locking down the role: {str(e)}",
                color=0xFF0000
            )
            await inter.edit_original_message(embed=error_embed)

    @commands.has_permissions(manage_roles=True, manage_channels=True)
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def unlockrole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = Param(description="Role to unlock"),
    ):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for channel in inter.guild.channels:
                await channel.set_permissions(role, send_messages=True)
            embed = disnake.Embed(
                title=STRINGS["moderation"]["lockdownliftedtitleone"],
                description=STRINGS["moderation"]["lockdownlifteddescone"],
                color=0x6E8F5D,
            )
            await inter.edit_original_message(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while unlocking the role: {str(e)}",
                color=0xFF0000
            )
            await inter.edit_original_message(embed=error_embed)

    @commands.has_permissions(manage_guild=True, manage_channels=True)
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True)
    async def lockdown(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for channel in inter.guild.channels:
                await channel.set_permissions(inter.guild.default_role, send_messages=False)
            embed = disnake.Embed(
                title=STRINGS["moderation"]["lockdowntitleone"],
                description=STRINGS["moderation"]["lockdowndescone"],
            )
            await inter.edit_original_message(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while locking down the server: {str(e)}",
                color=0xFF0000
            )
            await inter.edit_original_message(embed=error_embed)

    @commands.has_permissions(manage_guild=True, manage_channels=True)
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True)
    async def unlock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            for channel in inter.guild.channels:
                await channel.set_permissions(inter.guild.default_role, send_messages=True)
            embed = disnake.Embed(
                title=STRINGS["moderation"]["lockdownliftedtitleone"],
                description=STRINGS["moderation"]["lockdownlifteddescone"],
                color=0x6E8F5D,
            )
            await inter.edit_original_message(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while unlocking the server: {str(e)}",
                color=0xFF0000
            )
            await inter.edit_original_message(embed=error_embed)

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channellock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            await inter.channel.set_permissions(
                inter.guild.default_role, send_messages=False
            )
            embed = disnake.Embed(
                title=STRINGS["moderation"]["channellockdowntitle"],
                description=STRINGS["moderation"]["channellockdowndesc"],
                color=0x6E8F5D,
            )
            await inter.followup.send(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while locking the channel: {str(e)}",
                color=0xFF0000
            )
            await inter.followup.send(embed=error_embed)

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channelunlock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            s = await Settings(inter.guild.id)
            lang = await s.get_field("locale", CONFIG["default_locale"])
            STRINGS = Strings(lang)
            await inter.channel.set_permissions(
                inter.guild.default_role, send_messages=True
            )
            embed = disnake.Embed(
                title=STRINGS["moderation"]["channellockdownliftedtitle"],
                description=STRINGS["moderation"]["channellockdownlifteddesc"],
                color=0x6E8F5D,
            )
            await inter.followup.send(embed=embed)
        except Exception as e:
            error_embed = disnake.Embed(
                title="Error",
                description=f"An error occurred while unlocking the channel: {str(e)}",
                color=0xFF0000
            )
            await inter.followup.send(embed=error_embed)
            
def setup(bot: Bot) -> NoReturn:
    """

    :param bot: Bot:

    """
    bot.add_cog(Moderation(bot))
    Logger.cog_loaded(bot.get_cog("Moderation").name)
