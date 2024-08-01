import ast
import asyncio
import datetime
import math
import operator as op

import disnake
from disnake import ButtonStyle, SelectOption
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from disnake.ui import Button, Select, View

from scripts.calculator import buttons

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


class Calculator(commands.Cog, name="Calculator"):
    """ """

    def __init__(self, bot):
        self.bot = bot
        self.name = "Calculator"

    @commands.slash_command(name="calculator", description="Calculator")
    async def calculator(self, inter: disnake.ApplicationCommandInteraction):
        def eval_(node):
            """

            :param node: 

            """
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num)):
                raise ValueError("Invalid expression")
            match node:
                case ast.Constant(value) if isinstance(value, int):
                    return value  # integer
                case ast.BinOp(left, op, right):
                    return operators[type(op)](eval_(left), eval_(right))
                case ast.UnaryOp(op, operand):  # e.g., -1
                    return operators[type(op)](eval_(operand))
                case _:
                    raise TypeError(node)

        def calculate(exp):
            """Calculates the result of the given mathematical expression.

            :param exp: The mathematical expression to be evaluated.
            :type exp: str
            :returns: The result of the expression, or "An error occurred." if an error occurs during the calculation.
            :rtype: str

            """
            ox = "".join(filter(str.isdigit, exp))
            print(ox)
            o = ox.replace("×", "*")
            o = o.replace("÷", "/")
            o = o.replace("π", str(math.pi))
            o = o.replace("²", "**2")
            o = o.replace("³", "**3")
            result = ""
            try:
                result = eval_(ast.parse(int(o), mode="eval").body)
                print(result)
                result = str(result)
            except BaseException:
                result = "An error occurred."
            return result

        m = await inter.response.send_message(content="Loading Calculators...")
        expression = "None"
        delta = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
        e = disnake.Embed(
            title=f"{inter.author.name}'s calculator",
            description=f"\n{expression}",
            timestamp=delta,
            color=disnake.Colour.blurple(),
        )
        msg = await inter.original_response()
        await msg.edit(content="", components=buttons, embed=e)
        done = [
            [
                Button(style=ButtonStyle.grey, label="·", disabled=True),
            ]
        ]
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
        while msg.created_at < delta:
            try:
                res = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.author.id == inter.author.id
                    and i.message.id == msg.id,
                    timeout=(
                        delta - datetime.datetime.now(datetime.UTC)
                    ).total_seconds(),
                )
            except asyncio.TimeoutError:
                await msg.edit(
                    embed=disnake.Embed(
                        title="Closing down",
                        description="Calculator session timed out",
                        color=0xDD2E44,
                    ),
                    components=done,
                )
                break

            expression = res.message.embeds[0].description[6:-3]
            print(expression)
            if expression in ["None", "An error occurred."]:
                expression = ""
                print(expression)
            if res.component.label == "Exit":
                print(expression)
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
                print(expression)
                expression = expression[:-1]
            elif res.component.label == "Clear":
                expression = "None"
            elif res.component.label == "=":
                print(expression)
                result = calculate(expression)
                print(result)
                if result in ["None", "An error occurred."]:
                    await res.response.edit_message(
                        embed=disnake.Embed(
                            title=f"Error in calculation",
                            description=f"We havce encountered an error: {result}",
                            color=disnake.Colour.red(),
                        ),
                        components=done,
                    )
                    break
                else:
                    await res.response.edit_message(
                        embed=disnake.Embed(
                            title=f"{inter.author.name}'s calculator",
                            description=f"The expression you entered has a result of: {result}",
                            color=disnake.Colour.blurple(),
                        ),
                        components=done,
                    )
                break

            elif (
                len(expression) > 9
                or expression.count("²") >= 4
                or expression.count("³") >= 4
                or expression.count("²²") > 1
                or expression.count("³³") > 1
                or expression.count("²²³³") >= 1
            ):
                if res.component.label in allowed:
                    print(expression)
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
                    print(expression)
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
                expression += (
                    res.component.label
                    if res.component.label.isdigit()
                    or res.component.label
                    in [
                        "+",
                        "-",
                        "*",
                        "/",
                        ".",
                        "(",
                        ")",
                        "π",
                        "x²",
                        "x³",
                        "÷",
                        ".",
                        "×",
                    ]
                    else "Invalid expression"
                )
                print(expression)
                f = disnake.Embed(
                    title=f"{inter.author.name}'s calculator",
                    description=f"\n{expression}",
                    timestamp=delta,
                    color=disnake.Colour.blurple(),
                )
                await res.response.edit_message(embed=f, components=buttons)


def setup(bot):
    """

    :param bot: 

    """
    bot.add_cog(Calculator(bot))
