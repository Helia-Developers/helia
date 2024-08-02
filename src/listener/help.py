import disnake
from disnake import ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ui import Button, Select, View

class Dropdown(disnake.ui.Select):
    def __init__(self, options, bot):
        self.bot = bot
        super().__init__(
            placeholder="Select a category", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        label = self.values[0]
        for cog in self.bot.cogs:
            if label == cog:
                await get_help(self, interaction, CogToPassAlong=cog)
                return
        if label == "Close":
            embede = disnake.Embed(
                title=":books: Help System",
                description=f"Welcome To {self.bot.user.name} Help System",
            )
            embede.set_footer(text="Developed with ❤️ by Middlle")
            await interaction.response.edit_message(embed=embede, view=None)


class DropdownView(disnake.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        options = [SelectOption(label=cog, value=cog) for cog in bot.cogs if cog.lower() not in ["testingcog", "preferences", "calculator", "help","workers","jishaku","listeners","utils"]]
        options.append(SelectOption(label="Close", value="Close"))
        self.add_item(Dropdown(options, self.bot))


class PaginationView(disnake.ui.View):
    def __init__(self, embeds, bot):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        self.bot = bot
        self.add_item(Dropdown([SelectOption(label=cog, value=cog) for cog in bot.cogs if cog.lower() not in ["testingcog", "preferences", "calculator", "help","workers","jishaku","listeners","utils"]] + [SelectOption(label="Close", value="Close")], self.bot))
        self.add_item(Button(style=ButtonStyle.primary, label="◀", custom_id="previous"))
        self.add_item(Button(style=ButtonStyle.primary, label="▶", custom_id="next"))

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if interaction.data.custom_id == "previous":
            self.current_page = max(0, self.current_page - 1)
        elif interaction.data.custom_id == "next":
            self.current_page = min(len(self.embeds) - 1, self.current_page + 1)

        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        return True

class Help(commands.Cog):
    "The Help Menu Cog"

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Shows the help menu")
    async def help(
        self, inter: disnake.ApplicationCommandInteraction, command: str = None
    ):
        if command is None:
            await self.send_bot_help(inter)
        else:
            cmd = self.bot.get_slash_command(command)
            if cmd:
                await self.send_command_help(inter, cmd)
            else:
                await inter.response.send_message(
                    f"No command called '{command}' found.", ephemeral=True
                )

    async def send_bot_help(self, inter: disnake.ApplicationCommandInteraction):
        embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Developed with ❤️ by Middlle")
        view = DropdownView(self.bot)
        await inter.response.send_message(embed=embede, view=view)

    async def send_command_help(self, inter: disnake.ApplicationCommandInteraction, command):
        signature = f"/{command.name}"
        if isinstance(command, commands.InvokableSlashCommand):
            signature += f" {' '.join([f'<{param.name}>' for param in command.options])}"
        embed = HelpEmbed(
            title=signature, description=command.description or "No help found..."
        )

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        embed.add_field(name="Usable", value="Yes")

        if command._buckets and (cooldown := command._buckets._cooldown):
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await inter.response.send_message(embed=embed)

class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = disnake.utils.utcnow()
        self.set_footer(text="Developed with ❤️ by Middlle")

async def get_help(self, interaction, CogToPassAlong):
    cog = self.bot.get_cog(CogToPassAlong)
    if not cog:
        return
    embeds = []
    embed = disnake.Embed(
        title=f"{CogToPassAlong} - Commands",
        description=cog.__doc__,
    )
    embed.set_author(name="Help System")
    commands_text = ""
    for command in cog.get_slash_commands():
        command_text = f"『`/{command.name}`』: {command.description}\n"
        if len(commands_text) + len(command_text) > 1024:
            embed.add_field(name="Commands", value=commands_text, inline=False)
            embeds.append(embed)
            embed = disnake.Embed(
                title=f"{CogToPassAlong} - Commands (Continued)",
                description=cog.__doc__,
            )
            embed.set_author(name="Help System")
            commands_text = command_text
        else:
            commands_text += command_text
    if commands_text:
        embed.add_field(name="Commands", value=commands_text, inline=False)
    embeds.append(embed)
    
    if len(embeds) > 1:
        view = PaginationView(embeds, self.bot)
        await interaction.response.edit_message(embed=embeds[0], view=view)
    else:
        await interaction.response.edit_message(embed=embeds[0])


def setup(bot):
    bot.add_cog(Help(bot))
