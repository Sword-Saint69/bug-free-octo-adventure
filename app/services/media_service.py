from typing import Optional
from app.adapters.media import MediaAdapter
from app.schemas.dashboard import MediaPlayerModule

class MediaService:
    @classmethod
    async def get_media_player(cls) -> MediaPlayerModule:
        return await MediaAdapter.get_current_media()

    @classmethod
    async def update_media_player(
        cls,
        title: str,
        artist: str,
        album: Optional[str] = None,
        is_playing: bool = True,
        progress_ms: int = 0,
        duration_ms: int = 0,
        album_art_url: Optional[str] = None
    ) -> MediaPlayerModule:
        return await MediaAdapter.update_media_state(
            title=title,
            artist=artist,
            album=album,
            is_playing=is_playing,
            progress_ms=progress_ms,
            duration_ms=duration_ms,
            album_art_url=album_art_url
        )
