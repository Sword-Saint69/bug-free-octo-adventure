from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str

class StandardResponse(BaseModel, Generic[T]):
    request_id: str
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
