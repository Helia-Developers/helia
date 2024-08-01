"""
A cog that provides testing functionality for the Discord bot, including button and select menu interactions.

The `testingCOG` class provides two commands:

- `button`: Sends a message with a clickable button that responds with "Yay" when clicked.
- `select`: Sends an embed with a dropdown menu that allows the user to choose from various categories. Selecting a category will display a list of commands in that category.

The cog also includes the necessary setup function to add the cog to the bot.
"""
import disnake
from disnake import Button
from disnake import ButtonStyle
from disnake import SelectOption
from disnake.ext import commands
from disnake.ui import Select as Dropdown
from disnake.ui import View


class testingCOG(commands.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="button", description="BUTTON TEST")
    async def button(self, inter: disnake.ApplicationCommandInteraction):
        async def callback(interaction):
            await interaction.response.send_message(content="Yay")

        button = Button(style=ButtonStyle.blurple, label="Click this")
        button.callback = callback

        await inter.response.send_message("Button callbacks!", components=[button])


def setup(bot):
    """

    :param bot:

    """
    bot.add_cog(testingCOG(bot))
