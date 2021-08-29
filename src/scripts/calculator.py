import math

from discord_components import Button
from discord_components import ButtonStyle

buttons = [
    [
        Button(style=ButtonStyle.grey, label="1"),
        Button(style=ButtonStyle.grey, label="2"),
        Button(style=ButtonStyle.grey, label="3"),
        Button(style=ButtonStyle.blue, label="×"),
        Button(style=ButtonStyle.red, label="Exit"),
    ],
    [
        Button(style=ButtonStyle.grey, label="4"),
        Button(style=ButtonStyle.grey, label="5"),
        Button(style=ButtonStyle.grey, label="6"),
        Button(style=ButtonStyle.blue, label="÷"),
        Button(style=ButtonStyle.red, label="←"),
    ],
    [
        Button(style=ButtonStyle.grey, label="7"),
        Button(style=ButtonStyle.grey, label="8"),
        Button(style=ButtonStyle.grey, label="9"),
        Button(style=ButtonStyle.blue, label="+"),
        Button(style=ButtonStyle.red, label="Clear"),
    ],
    [
        Button(style=ButtonStyle.grey, label="00"),
        Button(style=ButtonStyle.grey, label="0"),
        Button(style=ButtonStyle.grey, label="."),
        Button(style=ButtonStyle.blue, label="-"),
        Button(style=ButtonStyle.green, label="="),
    ],
    [
        Button(style=ButtonStyle.grey, label="("),
        Button(style=ButtonStyle.grey, label=")"),
        Button(style=ButtonStyle.grey, label="π"),
        # Button(style=ButtonStyle.grey, label="x²"),
        # Button(style=ButtonStyle.grey, label="x³"),
    ],
]
