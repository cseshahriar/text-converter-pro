from pydantic import BaseModel, Field
from datetime import datetime


class ConversionRequest(BaseModel):
    text: str
    operation: str


class ConvertResponse(BaseModel):
    result: str


class APIKeyOut(BaseModel):
    key: str


class CreditRequestCreate(BaseModel):
    credits_requested: int


class CreditRequestOut(BaseModel):
    id: int
    user_id: int
    credits_requested: int
    status: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class CreditBalance(BaseModel):
    credits: int


class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    is_admin: bool
    is_verified: bool
    model_config = {
        "from_attributes": True
    }
    # It allows Pydantic to read data from object attributes instead of just dictionaries.
