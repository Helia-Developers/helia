import asyncio

import disnake
import youtube_dl
from disnake import User

from .utilities import parse_duration

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    "source_address": "0.0.0.0",
}

ffmpeg_options = {
    "before_options": "-re -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -nostats -loglevel 0",
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class AudioTrack(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1.0, requester: User = ""):
        super().__init__(source, volume=volume)

        self.title = data.get("title", "None")
        self.uploader = data.get("uploader", "None")
        self.url = data.get("webpage_url", "None")
        self.duration = parse_duration(int(data.get("duration", 0)))
        self.thumbnail = data.get(
            "thumbnail",
            "https://gallery.autodesk.com/assets/default%20tile%20thumbnail"
            "-dae75f5694cb3676feff44873695919704be92f0c54785a4ef95e1b750a94645.jpg",
        )
        self.extractor = data.get("extractor", "None")
        self.requester = requester

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, requester: User = ""):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            list_of_source = []
            for each_data in data["entries"]:
                filename = each_data["url"]
                source = cls(
                    disnake.FFmpegPCMAudio(filename, **ffmpeg_options),
                    data=each_data,
                    requester=requester,
                )
                list_of_source.append(source)

            return list_of_source

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return [
            cls(
                disnake.FFmpegPCMAudio(source=filename, **ffmpeg_options),
                data=data,
                requester=requester,
            )
        ]

    @classmethod
    async def from_keywords(
        cls, keywords, *, loop=None, stream=False, requester: User = ""
    ):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(f"ytsearch:{keywords}", download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return [
            cls(
                disnake.FFmpegPCMAudio(source=filename, **ffmpeg_options),
                data=data,
                requester=requester,
            )
        ]
