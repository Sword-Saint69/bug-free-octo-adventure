import uuid
from pydantic import BaseModel
from fastapi import APIRouter
from app.schemas.response import StandardResponse

router = APIRouter()

class PairingClaimRequest(BaseModel):
    claim_code: str
    device_name: str = "My Desk Display"

class PairingClaimResponse(BaseModel):
    device_id: str
    access_token: str
    status: str = "PAIRED"

@router.post("/pairing/claim", response_model=StandardResponse[PairingClaimResponse])
async def claim_device(payload: PairingClaimRequest):
    return StandardResponse(
        request_id=f"req_{uuid.uuid4().hex[:10]}",
        data=PairingClaimResponse(
            device_id=f"dev_{uuid.uuid4().hex[:12]}",
            access_token=f"token_{uuid.uuid4().hex[:16]}",
            status="PAIRED"
        )
    )
