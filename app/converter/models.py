from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from app.db.config import Base


class UserCredits(Base):
    __tablename__ = "user_credits"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),  unique=True
    )
    credits: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )


class APIKey(Base):
    __tablename__ = "api_keys"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )


class CreditRequest(Base):
    __tablename__ = "credit_requests"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    credits_requested: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=datetime.now(timezone.utc)
    )
