from disnake import VoiceClient

from listener.core.music.audio_event import AudioEventListener, DefaultTrackScheduler
from listener.core.music.audio_source import AudioTrack


class AudioPlayer:
    def __init__(
        self, voice_client: VoiceClient, event_listener: AudioEventListener = None
    ):
        self.voice_client = voice_client
        if event_listener is not None:
            self.scheduler = event_listener
        else:
            self.scheduler = DefaultTrackScheduler()

        self.scheduler.audio_player = self
        self.now_playing = None

    def bind_listener(self, event_listener: AudioEventListener):
        self.scheduler = event_listener
        self.scheduler.audio_player = self

    def play(self, audio_track: AudioTrack):
        self.voice_client.play(source=audio_track, after=self.scheduler.on_track_end)
        self.now_playing = audio_track
        self.scheduler.on_track_start(audio_track)
