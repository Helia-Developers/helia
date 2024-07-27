"""
A cog that provides testing functionality for the Discord bot, including button and select menu interactions.

The `testingCOG` class provides two commands:

- `button`: Sends a message with a clickable button that responds with "Yay" when clicked.
- `select`: Sends an embed with a dropdown menu that allows the user to choose from various categories. Selecting a category will display a list of commands in that category.

The cog also includes the necessary setup function to add the cog to the bot.
"""

import disnake
from disnake import Button, ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ui import Select as Dropdown
from disnake.ui import View


class testingCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="button", description="BUTTON TEST")
    async def button(self, inter: disnake.ApplicationCommandInteraction):
        async def callback(interaction):
            await interaction.response.send_message(content="Yay")

        button = Button(style=ButtonStyle.blurple, label="Click this")
        button.callback = callback

        await inter.response.send_message("Button callbacks!", components=[button])

    @commands.slash_command(name="select", description="SELECT TEST")
    async def select(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="SELECTION TEST", description="Testing our embeds", color=0xFF8000
        )
        embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Temporarily in testing")

        class DropdownView(View):
            def __init__(self):
                super().__init__()
                self.add_item(
                    Dropdown(
                        placeholder="Main Page",
                        options=[
                            SelectOption(label="General", value="General"),
                            SelectOption(label="Moderation", value="Moderation"),
                            SelectOption(label="Utilities", value="Utilities"),
                            SelectOption(label="Music", value="Music"),
                            SelectOption(label="Preferences", value="Preferences"),
                            SelectOption(label="Other", value="Other"),
                            SelectOption(label="Close", value="Close"),
                        ],
                    )
                )

            @disnake.ui.select()
            async def select_callback(
                self, select: Dropdown, interaction: disnake.MessageInteraction
            ):
                label = select.values[0]
                if label == "General":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "General":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)
                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":beginner: General",
                            description=f"Here is the list of general commands we have \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Moderation":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "Moderation":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)

                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":hammer_pick: Moderation",
                            description=f"Here is the list of moderation commands we have \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Utilities":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "Utilities":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)
                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":wrench: Utilities",
                            description=f"Here is the list of utilities commands we have \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Music":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "Music":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)
                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":headphones: Music",
                            description=f"Here is the list of music commands we have \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Preferences":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "Prefs":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)
                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":tools: Preferences",
                            description=f"Here is the list of bot configuration commands \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Other":
                    x = []
                    for y in self.bot.commands:
                        if y.cog and y.cog.qualified_name == "Other":
                            x.append(y.name)
                    formatlistprep = ":\n.".join(x)
                    await interaction.response.edit_message(
                        embed=disnake.Embed(
                            title=":hourglass: Other",
                            description=f"Here is the list of miscellaneous commads \n {formatlistprep}",
                        ).set_author(name="Help System"),
                    )
                elif label == "Close":
                    done_components = [
                        Button(style=ButtonStyle.grey, label="·", disabled=True),
                    ]
                    await interaction.response.edit_message(
                        embed=embede, components=done_components
                    )

        view = DropdownView()
        await inter.response.send_message(embed=embede, view=view)


def setup(bot):
    bot.add_cog(testingCOG(bot))
