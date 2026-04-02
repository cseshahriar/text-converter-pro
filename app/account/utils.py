import uuid
from sqlalchemy import select
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import RefreshToken, User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_tokens(db: AsyncSession, user: User):
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token_str = str(uuid.uuid4())
    expire_at = datetime.now(timezone.utc) + timedelta(days=7)
    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=expire_at
    )
    db.add(refresh_token)
    await db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }


async def verify_refresh_token(session: AsyncSession, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token and not db_token.revoked:
        expires_at = db_token.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at > datetime.now(timezone.utc):
            user_stmt = select(User).where(User.id == db_token.user_id)
            user_result = await session.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            return user

    return None


async def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def create_email_verification_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"sub": str(user_id), "type": "verify", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token_and_get_user_id(token: str, token_type: str):
    payload = await decode_token(token)
    if not payload or payload.get("type") != token_type:
        return None
    return int(payload.get("sub"))


async def get_user_by_email(session: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


def create_password_reset_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"sub": str(user_id), "type": "reset", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def revoke_refresh_token(session: AsyncSession, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()

    if db_token:
        db_token.revoked = True
        await session.commit()
