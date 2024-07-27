"""
The `Dropdown` class is a custom Discord UI component that provides a dropdown menu for users to select a category from a list of options. The selected category is then used to display the corresponding help information for that category.

The `DropdownView` class is a custom Discord UI view that contains the `Dropdown` component, allowing it to be displayed in a message.

The `get_help` function is responsible for generating the help embed that is displayed to the user based on the selected category. It retrieves the commands from the corresponding cog and formats them into an embed.

The `Help` class is a Discord bot cog that provides the `/help` command, which displays the help system to the user. It creates the initial help embed and the `DropdownView` to allow the user to select a category.
"""

import disnake
from disnake import ButtonStyle, SelectOption, interactions
from disnake.ext import commands
from disnake.ui import Button, Select, View


class Dropdown(disnake.ui.Select):

    def __init__(self, bot):
        self.bot = bot  # one thing fixed...

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label="General", value="General"),
            SelectOption(label="Moderation", value="Moderation"),
            SelectOption(label="Utilities", value="Utilities"),
            SelectOption(label="Music", value="Music"),
            SelectOption(label="Preferences", value="Preferences"),
            SelectOption(
                label="Welcome",
                value="Welcome",
            ),
            SelectOption(
                label="Goodbye",
                value="Goodbye",
            ),
            SelectOption(label="Other", value="Other"),
            SelectOption(label="Close", value="Close"),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder="Select a category",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: disnake.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        # print(f"{interaction.author.name} with ID {interaction.author.id} just clicked something in the select menu")
        label = self.values[0]
        print(label)
        for cog in self.bot.cogs:  # fixed
            if label == cog:  # -------------------[1]
                await get_help(self, interaction, CogToPassAlong=cog)
                print(str(cog))
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

        # Adds the dropdown to our view object.
        self.bot = bot
        self.add_item(Dropdown(self.bot))


async def get_help(self, interaction, CogToPassAlong):
    # if CogToPassAlong == "NSFW":
    # if not interaction.channel.is_nsfw():
    # embed = disnake.Embed(title="Non-NSFW channel 🔞", description=f"Find yourself an NSFW-Channel and retry from there.", color=disnake.Colour.red())
    # embed.set_footer(text=f"set_your_footer_here")
    # await interaction.respond(embed=embed)
    # return
    # else:
    # pass

    for _ in self.bot.get_cog(CogToPassAlong).get_commands():
        pass
    # making title - getting description from doc-string below class
    emb = disnake.Embed(
        title=f"{CogToPassAlong} - Commands",
        description=self.bot.cogs[CogToPassAlong].__doc__,
    )
    emb.set_author(name="Help System")
    # getting commands from cog
    for command in self.bot.get_cog(CogToPassAlong).get_commands():
        # if cog is not hidden
        if not command.hidden:
            emb.add_field(name=f"『`{command.name}`』",
                          value=command.help,
                          inline=False)
    # found cog - breaking loop
    await interaction.response.edit_message(embed=emb)


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(slash_command=True,
                      message_command=True,
                      description="Help Command")
    async def help(self, ctx):
        embed = disnake.Embed(title="SELECTION TEST",
                              description="Testing our embeds",
                              color=0xFF8000)
        embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Developed with ❤️ by Middlle")
        view = DropdownView(self.bot)

        done_components = [
            Button(style=ButtonStyle.secondary, label="·", disabled=True),
        ]

        # async def callback(interaction):
        # await interaction.send(embed=embed)

        await ctx.send(embed=embede, view=view)

    @commands.slash_command(
        name="help",
        description="Get a list of commands in the bot.",
    )
    async def shelp(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="SELECTION TEST",
                              description="Testing our embeds",
                              color=0xFF8000)
        embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Developed with ❤️ by Middlle")
        view = DropdownView(self.bot)

        done_components = [
            Button(style=ButtonStyle.secondary, label="·", disabled=True),
        ]

        # async def callback(interaction):
        # await interaction.send(embed=embed)

        await inter.response.send_message(embed=embede, view=view)


def setup(bot):
    bot.add_cog(Help(bot))
