from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.account.models import User
from app.converter.models import (
    UserCredits, APIKey, CreditRequest
)
from app.converter.utils import generate_api_key, convert_text
from app.converter.schemas import ConversionRequest
from app.converter.dependencies import get_user_from_api_key


async def generate_user_api_key(session: AsyncSession, user: User):
    await session.execute(delete(APIKey).where(APIKey.user_id == user.id))
    api_key = generate_api_key()
    new_api_key = APIKey(user_id=user.id, key=api_key)
    session.add(new_api_key)
    await session.commit()
    await session.refresh(new_api_key)
    return api_key


async def get_user_api_key(session: AsyncSession, user: User):
    key_obj = await session.scalar(select(APIKey).where(APIKey.user_id == user.id))
    if not key_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
        )
    return key_obj.key


async def get_or_create_user_credits(session: AsyncSession, user_id: int):
    credit_obj = await session.scalar(select(UserCredits).where(UserCredits.user_id == user_id))
    if not credit_obj:
        credit_obj = UserCredits(user_id=user_id, credits=10)  # Initial credits
        session.add(credit_obj)
        await session.commit()
        await session.refresh(credit_obj)
    return credit_obj


async def get_or_credit_request_list(session: AsyncSession, user: User):
    result = await session.execute(
        select(CreditRequest).order_by(CreditRequest.created_at.desc())
    )
    return result.scalars().all()


async def submit_credit_request(
    session: AsyncSession, user: User, credits: int
):
    req = CreditRequest(
        user_id=user.id, credits_requested=credits, status='pending'
    )
    session.add(req)
    await session.commit()
    await session.refresh(req)
    return req


async def approved_credit_request(session: AsyncSession, request_id: int):
    req = await session.get(CreditRequest, request_id)
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credit request not found"
        )

    if req.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request already processed"
        )

    credit_obj = await get_or_create_user_credits(session, req.user_id)
    credit_obj.credits += req.credits_requested
    req.status = 'approved'
    await session.commit()
    await session.refresh(credit_obj)
    return req


async def handle_conversion(
    session: AsyncSession,
    data: ConversionRequest,
    user: User,
):
    credit_obj = await get_or_create_user_credits(session, user.id)
    if credit_obj.credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits"
        )

    try:
        converted = convert_text(data.text, data.operation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    credit_obj.credits -= 1
    await session.commit()
    await session.refresh(credit_obj)
    return converted
