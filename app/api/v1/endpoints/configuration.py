import uuid
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.response import StandardResponse
from app.services.config_service import ConfigService

router = APIRouter()


class ConfigurationUpdate(BaseModel):
    OPENAQ_API_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    NASA_API_KEY: Optional[str] = None
    DEFAULT_LATITUDE: Optional[float] = Field(None, ge=-90, le=90)
    DEFAULT_LONGITUDE: Optional[float] = Field(None, ge=-180, le=180)
    DEFAULT_COUNTRY_CODE: Optional[str] = Field(None, min_length=2, max_length=2)


def authorize(authorization: str) -> None:
    expected = f"Bearer {settings.SECRET_KEY}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Invalid console access token")


@router.get("/configuration", response_model=StandardResponse[dict], summary="Read masked runtime configuration")
async def get_configuration(authorization: str = Header(...)):
    authorize(authorization)
    return StandardResponse(request_id=f"req_{uuid.uuid4().hex[:10]}", data=ConfigService.snapshot())


@router.put("/configuration", response_model=StandardResponse[dict], summary="Update runtime configuration")
async def update_configuration(payload: ConfigurationUpdate, authorization: str = Header(...)):
    authorize(authorization)
    values = payload.model_dump(exclude_none=True)
    if "DEFAULT_COUNTRY_CODE" in values:
        values["DEFAULT_COUNTRY_CODE"] = values["DEFAULT_COUNTRY_CODE"].upper()
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=ConfigService.update(values),
    )
