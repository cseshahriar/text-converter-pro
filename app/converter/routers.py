from fastapi import APIRouter, Depends
from typing import List
from app.converter.schemas import (
    APIKeyOut, CreditBalance, CreditRequestOut, CreditRequestCreate,
    ConversionRequest
)
from app.db.config import SessionDep
from app.account.models import User
from app.converter.services import (
    generate_user_api_key,
    get_user_api_key,
    get_or_create_user_credits,
    get_or_credit_request_list,
    submit_credit_request,
    approved_credit_request,
    handle_conversion
)
from app.account.dependencies import get_current_user, require_admin
from app.converter.dependencies import get_user_from_api_key


router = APIRouter()


@router.post("/generate-api-key", response_model=APIKeyOut)
async def generate_api_key(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    api_key = await generate_user_api_key(session, current_user)
    return {"key": api_key}


@router.get("/my/api-key", response_model=APIKeyOut)
async def get_api_key(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    api_key = await get_user_api_key(session, current_user)
    return {"key": api_key}


@router.get("/my/credits", response_model=CreditBalance)
async def get_credits(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    credit_obj = await get_or_create_user_credits(session, current_user.id)
    return {"credits": credit_obj.credits}


@router.get("/credit-requests", response_model=List[CreditRequestOut])
async def list_requests(
    session: SessionDep,
    user: User = Depends(require_admin)
):
    requests = await get_or_credit_request_list(session, user)
    return requests


@router.post("/buy-credit", response_model=CreditRequestOut)
async def buy_credits(
    session: SessionDep,
    data: CreditRequestCreate,
    current_user: User = Depends(get_current_user)
):
    req = await submit_credit_request(
        session, current_user, data.credits_requested
    )
    return req


@router.post("/approve-credit/{request_id}")
async def approve_request(
    session: SessionDep,
    request_id: int,
    user: User = Depends(require_admin)
):
    await approved_credit_request(session, request_id)
    return {"detail": "Request approved"}


@router.post("/convert")
async def convert_text_endpoint(
    session: SessionDep,
    data: ConversionRequest,
    current_user: User = Depends(get_user_from_api_key)  # require api key for conversion
):
    result = await handle_conversion(
        session,  data, current_user
    )
    return {"converted_text": result}
