import disnake
from disnake.ext import commands
from disnake_components import Button, ButtonStyle, Select, SelectOption


class testingCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        slash_interaction=False, message_command=True, description="BUTTON TEST"
    )
    async def button(self, ctx):
        async def callback(interaction):
            await interaction.send(content="Yay")

        await ctx.send(
            "Button callbacks!",
            components=[
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label="Click this"), callback
                ),
            ],
        )

    @commands.command(
        slash_interaction=False, message_command=True, description="SELECT TEST"
    )
    async def select(self, ctx):
        embed = disnake.Embed(
            title="SELECTION TEST", description="Testing our embeds", color=0xFF8000
        )
        embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Temporarily in testing")
        components = [
            Select(
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
        ]
        done_components = [
            [
                Button(style=ButtonStyle.grey, label="·", disabled=True),
            ]
        ]

        async def callback(interaction):
            await interaction.send(embed=embed)

        await ctx.send(embed=embede, components=components)

        while True:
            interaction = await self.bot.wait_for("select_option")
            label = interaction.values[0]
            if label == "General":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "General":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":beginner: General",
                        description=f"Here is the list of general commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Moderation":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Moderation":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)

                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":hammer_pick: Moderation",
                        description=f"Here is the list of moderation commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Utilities":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Utilities":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":wrench: Utilities",
                        description=f"Here is the list of utilities commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Music":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Music":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":headphones: Music",
                        description=f"Here is the list of music commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Preferences":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Prefs":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":tools: Preferences",
                        description=f"Here is the list of bot configuration commands \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Other":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Other":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.respond(
                    type=7,
                    embed=disnake.Embed(
                        title=":hourglass: Other",
                        description=f"Here is the list of miscellaneous commads \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
            if label == "Close":
                await interaction.respond(
                    type=7, embed=embede, components=done_components
                )


def setup(bot):
    bot.add_cog(testingCOG(bot))
