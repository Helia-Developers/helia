import disnake
from disnake import interactions
from disnake.ext import commands
from disnake import SelectOption,ButtonStyle
from disnake.ui import View, Select,Button

async def get_help(self, interaction, CogToPassAlong):
     #if CogToPassAlong == "NSFW":
        #if not interaction.channel.is_nsfw():
           #embed = disnake.Embed(title="Non-NSFW channel 🔞", description=f"Find yourself an NSFW-Channel and retry from there.", color=disnake.Colour.red())
            #embed.set_footer(text=f"set_your_footer_here")
            #await interaction.respond(embed=embed)
            #return
        #else:
            #pass
     if CogToPassAlong == "Welcome & Goodbye Messages":
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
            embed=disnake.Embed(
                title=":wave: Welcome & Goodbye Messages",
                description=f"{descwelcgood}",
            ).set_author(name="Help System")
        )
     else:
        pass

     for command in self.bot.get_cog(CogToPassAlong).get_commands():
        if command is not None:
            pass
    
     # making title - getting description from doc-string below class
     emb = disnake.Embed(title=f'{CogToPassAlong} - Commands', description=self.bot.cogs[CogToPassAlong].__doc__)
     emb.set_author(name="Help System")
     # getting commands from cog
     for command in self.bot.get_cog(CogToPassAlong).get_commands():
        # if cog is not hidden
        if not command.hidden:
            emb.add_field(name=f"『`{command.name}`』", value=command.help, inline=False)
     # found cog - breaking loop
     await interaction.response.edit_message(embed=emb)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.Interaction):
      embede = disnake.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
      #print(f"{interaction.author.name} with ID {interaction.author.id} just clicked something in the select menu")
      label = interaction.data.values[0]
      print(label)
      for cog in self.bot.cogs:
            if label == cog:#-------------------[1]
                await get_help(self, interaction, CogToPassAlong=cog)
                print(str(cog))
      if label == "Close":
                await interaction.response.edit_message(
                                          embed=embede,
                                          view=None)

      
    @commands.command(slash_interaction=True, message_command=True,description="Help Command")
    async def help(self, ctx):
        embed = disnake.Embed(title="SELECTION TEST",
                              description="Testing our embeds",
                              color=0xFF8000)
        embede = disnake.Embed(
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
        view = disnake.ui.View()
        selecter = disnake.ui.Select(placeholder='Select a category', min_values=1, max_values=1, options=options,custom_id="helpmenuer")
        view.add_item(selecter)
        
        done_components = [
            Button(style=ButtonStyle.secondary, label="·", disabled=True),
        ]

        #async def callback(interaction):
            #await interaction.send(embed=embed)

        await ctx.send(embed=embede, view=view)
        

        
            
        


def setup(bot):
    bot.add_cog(Help(bot))
