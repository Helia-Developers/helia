import disnake
from disnake import Embed


class CustomEmbed(Embed):

    def __init__(self):
        super().__init__(color=disnake.Color(value=1).lighter_grey())
