import disnake
from disnake import ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ui import Button, Select, View

class Dropdown(disnake.ui.Select):
    def __init__(self, options, bot):
        self.bot = bot
        super().__init__(placeholder="Select a category", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: disnake.MessageInteraction):
        label = self.values[0]
        for cog in self.bot.cogs:
            if label == cog:
                await get_help(self, interaction, CogToPassAlong=cog)
        if label == "Close":
            embede = disnake.Embed(
                title=":books: Help System",
                description=f"Welcome To {self.bot.user.name} Help System",
            )
            embede.set_footer(text="Developed with ❤️ by Middlle")
            await interaction.response.edit_message(embed=embede, view=None)

class DropdownView(disnake.ui.View):
    def __init__(self, options, bot):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown(options, self.bot))

class Help(commands.Cog):
    "The Help Menu Cog"

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Shows the help menu")
    async def help(self, inter: disnake.ApplicationCommandInteraction, command: str = None):
        if command is None:
            await self.send_bot_help(inter)
        else:
            await self.send_command_help(inter, command)

    async def send_bot_help(self, inter: disnake.ApplicationCommandInteraction):
        embed = HelpEmbed(description=f"Welcome To {self.bot.user.name} Help System")
        usable = 0
        myoptions = []

        filtered_cogs = ['testingCOG', 'Preferences', 'Calculator', 'Help']

        for cog_name, cog in self.bot.cogs.items():
            print(cog_name)
            if cog_name.lower() not in [fc.lower() for fc in filtered_cogs]:
                print(filtered_cogs)
                if filtered_commands := [cmd for cmd in cog.get_slash_commands()]:
                    amount_commands = len(filtered_commands)
                    usable += amount_commands
                    name = cog.qualified_name
                    description = cog.description or "No description"
                    myoptions.append(SelectOption(label=name, value=name))

        myoptions.append(SelectOption(label="Close", value="Close"))
        view = DropdownView(myoptions, self.bot)

        await inter.response.send_message(embed=embed, view=view)

    async def send_command_help(self, inter: disnake.ApplicationCommandInteraction, command_name: str):
        command = self.bot.get_slash_command(command_name)
        if not command:
            await inter.response.send_message(f"No command called '{command_name}' found.", ephemeral=True)
            return

        signature = f"/{command.name} {command.signature}"
        embed = HelpEmbed(title=signature, description=command.description or "No help found...")

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
        self.title = ":books: Help System"
        
        self.set_footer(text="Developed with ❤️ by Middlle")

async def get_help(self, interaction, CogToPassAlong):
    cog = self.bot.get_cog(CogToPassAlong)
    if not cog:
        return
    emb = disnake.Embed(
        title=f"{CogToPassAlong} - Commands",
        description=cog.__doc__,
    )
    emb.set_author(name="Help System")
    for command in cog.get_slash_commands():
        
            emb.add_field(
                name=f"『`/{command.name}`』", value=command.description, inline=False
            )
    await interaction.response.edit_message(embed=emb)

def setup(bot):
    bot.add_cog(Help(bot))
