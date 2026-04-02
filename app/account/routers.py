from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import SessionDep
from app.account.schemas import UserCreate, UserOut
from app.account.services import (
    create_user, authenticate_user,
    process_email_verification, verify_email_token,
    change_password,
    process_password_reset,
    reset_password_with_token
)
from app.account.utils import (
    create_tokens, verify_refresh_token,
    revoke_refresh_token
)
from app.account.dependencies import get_current_user, require_admin

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(session: SessionDep, user: UserCreate):
    ''' User registration api'''
    # Service must be awaited
    return await create_user(session, user)


@router.post("/login")
async def login(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):
    'User Login api'
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # If create_tokens performs DB ops (like saving a refresh token), await it
    tokens = await create_tokens(session, user)

    response = JSONResponse(content={"access_token": tokens["access_token"]})
    response.set_cookie(
        "refresh_token",
        tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )
    return response


@router.post("/refresh")
async def generate_refresh_token_api(session: SessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token.")

    user = await verify_refresh_token(session, token)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid or expired refresh token")

    return await create_tokens(session, user)


@router.get("/me", response_model=UserOut)
async def get_current_user_data(user=Depends(get_current_user)):
    return user


@router.post("/verify-request")
async def send_email_verification_link(user=Depends(get_current_user)):
    'Send verification link'
    return await process_email_verification(user)


@router.get("/verify")
async def verify_email_verification_token(session: SessionDep, token: str):
    'Verification email verification token'
    return await verify_email_token(session, token)


@router.post("/change-password")
async def password_change(
    session: SessionDep, new_password: str, user=Depends(get_current_user)
):
    await change_password(session, user, new_password)
    return {"msg": "Password changed successfully."}


@router.post("/forget-password")
async def forgot_password(session: SessionDep, email: str):
    'Password reset token send api'
    return await process_password_reset(session, email)


@router.post("/reset-password")
async def reset_password(session: SessionDep, token: str, new_password: str):
    return await reset_password_with_token(session, token, new_password)


@router.get("/admin")
async def get_admin_user_data(user=Depends(require_admin)):
    return {"msg": f"Welcome Admin {user.name}"}


@router.post("/logout")
async def logout(session: SessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if token:
        await revoke_refresh_token(session, token)

    response = JSONResponse(content={"detail": "Logged out"})
    response.delete_cookie("refresh_token")
    return response
