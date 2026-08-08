import uuid
from typing import Optional, Any, Dict
from pydantic import BaseModel
from fastapi import APIRouter, Header
from app.schemas.response import StandardResponse
from app.schemas.dashboard import MediaPlayerModule
from app.services.tasks_service import TasksService
from app.services.media_service import MediaService

router = APIRouter()

class DeviceActionRequest(BaseModel):
    action_type: str
    target_id: str
    params: Optional[Dict[str, Any]] = None

class DeviceActionResponse(BaseModel):
    action_id: str
    status: str = "COMPLETED"
    audit_event_logged: bool = True

class MediaUpdateRequest(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    is_playing: bool = True
    progress_ms: int = 0
    duration_ms: int = 0
    album_art_url: Optional[str] = None

@router.post("/device/actions", response_model=StandardResponse[DeviceActionResponse])
async def execute_device_action(
    payload: DeviceActionRequest,
    x_idempotency_key: str = Header(...),
    authorization: str = Header(...),
    x_device_id: str = Header(...)
):
    action_id = f"act_{uuid.uuid4().hex[:12]}"
    if payload.action_type in ("TASK_COMPLETE", "TASK_TOGGLE"):
        await TasksService.toggle_task(payload.target_id)
    
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=DeviceActionResponse(
            action_id=action_id,
            status="COMPLETED",
            audit_event_logged=True
        )
    )

@router.post("/actions/media", response_model=StandardResponse[MediaPlayerModule], summary="Push Spotify / Media Player status to Display")
async def update_media_player_status(
    payload: MediaUpdateRequest,
    authorization: str = Header(...)
):
    updated = await MediaService.update_media_player(
        title=payload.title,
        artist=payload.artist,
        album=payload.album,
        is_playing=payload.is_playing,
        progress_ms=payload.progress_ms,
        duration_ms=payload.duration_ms,
        album_art_url=payload.album_art_url
    )
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=updated
    )
