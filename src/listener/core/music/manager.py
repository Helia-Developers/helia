from .audio_event import AudioTrackScheduler


class GuildVoiceState:

    def __init__(self, client):
        self.volume = 1.0
        self.scheduler = AudioTrackScheduler(client=client)
        self.voice_client = None
        self.waiter = None
        self.waiting = False

    def cleanup(self):
        """Clears queue"""

        for source in self.scheduler.queue:
            source.cleanup()

        print("Cleanup queue")


class GuildMusicManager:

    def __init__(self, client):
        self.client = client
        self.guild_voice_states = {}

    def get_guild_state(self, guild_id) -> GuildVoiceState:
        """Gets Guild's Voice State"""

        if guild_id not in self.guild_voice_states:
            self.guild_voice_states[guild_id] = GuildVoiceState(
                client=self.client)

        return self.guild_voice_states[guild_id]
