import discord
from discord import interactions
from discord.ext import commands
from discord import SelectOption,ButtonStyle
from discord.ui import View, Select,Button



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
      print(f"{interaction.author.name} with ID {interaction.author.id} just clicked something in the select menu")
      label = interaction.data.values[0]
      if label.values[0] == "General":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "General":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":beginner: General",
                        description=f"Here is the list of general commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Moderation":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Moderation":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)

                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":hammer_pick: Moderation",
                        description=f"Here is the list of moderation commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Utilities":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Utilities":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":wrench: Utilities",
                        description=f"Here is the list of utilities commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Music":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Music":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":headphones: Music",
                        description=f"Here is the list of music commands we have \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Preferences":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Prefs":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":tools: Preferences",
                        description=f"Here is the list of bot configuration commands \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )

      if label.values[0] == "Welcome & Goodbye Messages":
                descwelcgood = """
                Here is the list of commands related to server join and leave messages
                ```welcome - Displays this message```
                .
                ```welcome channel [#channel mention] - Set welcome channel```
                .
                ```welcome clear - Remove the set welcome channel```
                .
                ```welcome text {Optionally enter text - otherwise the default will be set} - Set welcome text```
                .
                ```goodbye - Displays this message```
                .
                ```goodbye channel [#channel mention] - Set goodbye channel```
                .
                ```goodbye clear - Remove the set goodbye channel```
                .
                ```goodbye text {Optionally enter text - otherwise the default will be set} - Set goodbye text```

                """
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":wave: Welcome & Goodbye Messages",
                        description=f"{descwelcgood}",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Other":
                x = []
                for y in self.bot.commands:
                    if y.cog and y.cog.qualified_name == "Other":
                        x.append(y.name)
                formatlistprep = ":\n```.```".join(x)
                await interaction.response.edit_message(
                    
                    embed=discord.Embed(
                        title=":hourglass: Other",
                        description=f"Here is the list of miscellaneous commands \n ```{formatlistprep}```",
                    ).set_author(name="Help System"),
                )
      if label.values[0] == "Close":
                await interaction.response.edit_message(
                                          embed=embede,
                                          view=None)

      
    @commands.command(slash_interaction=True, message_command=True,description="Help Command")
    async def help(self, ctx):
        embed = discord.Embed(title="SELECTION TEST",
                              description="Testing our embeds",
                              color=0xFF8000)
        embede = discord.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Developed with ❤️ by Middlle")
        options=[
                    SelectOption(label="General", value="General"),
                    SelectOption(label="Moderation", value="Moderation"),
                    SelectOption(label="Utilities", value="Utilities"),
                    SelectOption(label="Music", value="Music"),
                    SelectOption(label="Preferences", value="Preferences"),
                    SelectOption(
                        label="Welcome & Goodbye Messages",
                        value="Welcome & Goodbye Messages",
                    ),
                    SelectOption(label="Other", value="Other"),
                    SelectOption(label="Close", value="Close"),
                ]
        view = discord.ui.View()
        selecter = discord.ui.Select(placeholder='Select a category', min_values=1, max_values=1, options=options,custom_id="helpmenuer")
        view.add_item(selecter)
        
        done_components = [
            Button(style=ButtonStyle.secondary, label="·", disabled=True),
        ]

        #async def callback(interaction):
            #await interaction.send(embed=embed)

        await ctx.send(embed=embede, view=view)
        

        
            
        


def setup(bot):
    bot.add_cog(Help(bot))
