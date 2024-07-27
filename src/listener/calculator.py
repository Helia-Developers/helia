import asyncio
import datetime
import math

import disnake
from disnake import ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from disnake.ui import Button, Select, View

from scripts.calculator import buttons


class Calculator(commands.Cog, name="Calculator"):

    def __init__(self, bot):
        self.bot = bot
        self.name = "Calculator"

    @commands.slash_command(name="calculator", description="Open a calculator")
    async def calculator(self, inter: disnake.ApplicationCommandInteraction):

        def calculate(exp):
            ox = str(exp)
            o = ox.replace("×", "*")
            o = o.replace("÷", "/")
            o = o.replace("π", str(math.pi))
            result = ""
            try:
                result = str(eval(o))
            except BaseException:
                result = "An error occurred."
            return result

        m = await inter.response.send_message(content="Loading Calculators...")
        expression = "None"
        delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        e = disnake.Embed(
            title=f"{inter.author.name}'s calculator",
            description=f"\n{expression}",
            timestamp=delta,
            color=disnake.Colour.blurple(),
        )
        await m.edit(content="", components=buttons, embed=e)
        done = [[
            Button(style=ButtonStyle.grey, label="·", disabled=True),
        ]]
        allowed = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "00",
            "0",
            ".",
            "(",
            ")",
            "π",
            "x²",
            "x³",
        ]
        while m.created_at < delta:
            try:
                res = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.author.id == inter.author.id and i.
                    message.id == m.id,
                    timeout=(delta -
                             datetime.datetime.utcnow()).total_seconds(),
                )
            except asyncio.TimeoutError:
                await m.edit(
                    embed=disnake.Embed(
                        title="Closing down",
                        description="Calculator session timed out",
                        color=0xDD2E44,
                    ),
                    components=done,
                )
                break

            expression = res.message.embeds[0].description[6:-3]
            if expression in ["None", "An error occurred."]:
                expression = ""
            if res.component.label == "Exit":
                await res.response.edit_message(
                    embed=disnake.Embed(
                        title="Closing down",
                        description="Calculator was terminated",
                        color=0xDD2E44,
                    ),
                    components=done,
                )
                break
            elif res.component.label == "←":
                expression = expression[:-1]
            elif res.component.label == "Clear":
                expression = "None"
            elif res.component.label == "=":
                expression = calculate(expression)
                await res.response.edit_message(
                    embed=disnake.Embed(
                        title=f"{inter.author.name}'s calculator",
                        description=f" expression you entered has a result of : {expression}",
                        color=disnake.Colour.blurple(),
                    ),
                    components=done,
                )
            elif (len(expression) > 9 or expression.count("²") >= 4
                  or expression.count("³") >= 4 or expression.count("²²") > 1
                  or expression.count("³³") > 1
                  or expression.count("²²³³") >= 1):
                if res.component.label in allowed:
                    await res.response.edit_message(
                        embed=disnake.Embed(
                            title="Closing down",
                            description="You have entered a number that is 9 or more in length or some calculation prone to crashing the bot - for the stability of the bot and crash prevention we will close down this calculator session",
                            color=0xDD2E44,
                        ),
                        components=done,
                    )
                    break
                elif expression.count("××") > 1:
                    await res.response.edit_message(
                        embed=disnake.Embed(
                            title="Closing down",
                            description="You have entered a number that is 9 or more in length or some calculation prone to crashing the bot - for the stability of the bot and crash prevention we will close down this calculator session",
                            color=0xDD2E44,
                        ),
                        components=done,
                    )
                    break
            else:
                expression += res.component.label
                f = disnake.Embed(
                    title=f"{inter.author.name}'s calculator",
                    description=f"\n{expression}",
                    timestamp=delta,
                    color=disnake.Colour.blurple(),
                )
                await res.response.edit_message(embed=f, components=buttons)


def setup(bot):
    bot.add_cog(Calculator(bot))
