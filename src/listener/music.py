import asyncio
import random
import re
import typing as t
from enum import Enum

import disnake
import wavelink
from disnake.ext import commands

from listener.utils import Config, Logger, Settings, Strings

CONFIG = Config()

URL_REGEX = (
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»"
    "'']))"
)

OPTIONS = {
    "1️⃣": 0,
    "2️⃣": 1,
    "3️⃣": 2,
    "4️⃣": 3,
    "5️⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    """ """

    pass


class NoVoiceChannel(commands.CommandError):
    """ """

    pass


class QueueIsEmpty(commands.CommandError):
    """ """

    pass


class NoTracksFound(commands.CommandError):
    """ """

    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    """ """

    pass


class PlayerIsAlreadyPlaying(commands.CommandError):
    """ """

    pass


class NoMoreTracks(commands.CommandError):
    """ """

    pass


class NoPreviousTracks(commands.CommandError):
    """ """

    pass


class InvalidRepeatMode(commands.CommandError):
    """ """

    pass


class RepeatMode(Enum):
    """ """

    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    """ """

    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        """ """
        return not self._queue

    @property
    def current_track(self):
        """ """
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        """ """
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[self.position + 1:]

    @property
    def history(self):
        """ """
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[: self.position]

    @property
    def length(self):
        """ """
        return len(self._queue)

    def add(self, *args):
        """

        :param *args:

        """
        self._queue.extend(args)

    def get_next_track(self):
        """ """
        if not self._queue:
            raise QueueIsEmpty
        self.position += 1
        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None
        return self._queue[self.position]

    def shuffle(self):
        """ """
        if not self._queue:
            raise QueueIsEmpty
        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[: self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        """

        :param mode:

        """
        if mode == "noloop":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "onesong":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "entirequeue":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        """ """
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
        elif (track := await self.choose_track(ctx, tracks)) is not None:
            self.queue.add(track)

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            """

            :param r:
            :param u:

            """
            return (
                r.emoji in OPTIONS.keys() and u == ctx.author and r.message.id == msg.id
            )

        embed = disnake.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length % 60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            color=disnake.Color.green(),
            timestamp=ctx.message.created_at,
        )
        embed.set_author(name="Search Results")
        embed.set_footer(text=f"Invoked by {ctx.author.name}")

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[: min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=_check
            )
        except asyncio.TimeoutError:
            await msg.delete()
            return None
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog):
    """Music commands for playing audio in voice channels."""

    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            not member.bot
            and after.channel is None
            and not [m for m in before.channel.members if not m.bot]
        ):
            await self.get_player(member.guild).teardown()

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: Player, track: wavelink.Track, reason
    ):
        if player.queue.repeat_mode == RepeatMode.ONE:
            await player.repeat_track()
        else:
            await player.advance()

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "n17.danbot.host",
                "port": 1679,
                "rest_uri": "http://n17.danbot.host:1679",
                "password": "DBH",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        """

        :param obj:

        """
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, disnake.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.slash_command(name="join", description="Join")
    async def join(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        channel = inter.author.voice.channel
        await player.connect(inter, channel)
        await inter.response.send_message(f"Joined {channel.name}")

    @commands.slash_command(name="leave", description="Leave")
    async def leave(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        await player.teardown()
        await inter.response.send_message("Left the voice channel")

    @commands.slash_command(name="play", description="Play")
    async def play(self, inter: disnake.ApplicationCommandInteraction, *, query: str):
        player = self.get_player(inter)

        if not player.is_connected:
            await player.connect(inter)

        query = query.strip("<>")
        if not re.match(URL_REGEX, query):
            query = f"ytsearch:{query}"

        await player.add_tracks(inter, await self.wavelink.get_tracks(query))
        await inter.response.send_message(f"Added to queue: {query}")

    @commands.slash_command(name="pause", description="Pause")
    async def pause(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        await player.set_pause(True)
        await inter.response.send_message("Paused the song")

    @commands.slash_command(name="resume", description="Resume")
    async def resume(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        await player.set_pause(False)
        await inter.response.send_message("Resumed the song")

    @commands.slash_command(name="stop", description="Stop")
    async def stop(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        player.queue.empty()
        await player.stop()
        await inter.response.send_message("Stopped the player and cleared the queue")

    @commands.slash_command(name="skip", description="Skip")
    async def skip(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        await player.stop()
        await inter.response.send_message("Skipped the current song")

    @commands.slash_command(name="queue", description="Queue")
    async def queue(self, inter: disnake.ApplicationCommandInteraction):
        player = self.get_player(inter)
        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = disnake.Embed(title="Queue", color=disnake.Color.blurple())
        embed.add_field(
            name="Currently playing",
            value=player.queue.current_track.title,
            inline=False,
        )

        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(
                    f"**{i+1}.** {t.title}" for i, t in enumerate(upcoming[:10])
                ),
                inline=False,
            )

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="volume", description="Volume")
    async def volume(self, inter: disnake.ApplicationCommandInteraction, volume: int):
        if not 0 <= volume <= 100:
            raise commands.BadArgument("Volume must be between 0 and 100")

        player = self.get_player(inter)
        await player.set_volume(volume)
        await inter.response.send_message(f"Volume set to {volume}%")


def setup(bot):
    """

    :param bot:

    """
    bot.add_cog(Music(bot))
    Logger.cog_loaded(bot.get_cog("Music").name)
