from typing import Optional
from app.schemas.dashboard import MediaPlayerModule

class MediaAdapter:
    # Live playback state store (starts idle with no fake tracks)
    _current_playback: MediaPlayerModule = MediaPlayerModule(
        title="",
        artist="",
        album=None,
        is_playing=False,
        progress_ms=0,
        duration_ms=0,
        album_art_url=None
    )

    @classmethod
    async def get_current_media(cls) -> MediaPlayerModule:
        return cls._current_playback

    @classmethod
    async def update_media_state(
        cls,
        title: str,
        artist: str,
        album: Optional[str] = None,
        is_playing: bool = True,
        progress_ms: int = 0,
        duration_ms: int = 0,
        album_art_url: Optional[str] = None
    ) -> MediaPlayerModule:
        cls._current_playback = MediaPlayerModule(
            title=title,
            artist=artist,
            album=album,
            is_playing=is_playing,
            progress_ms=progress_ms,
            duration_ms=duration_ms,
            album_art_url=album_art_url
        )
        return cls._current_playback
