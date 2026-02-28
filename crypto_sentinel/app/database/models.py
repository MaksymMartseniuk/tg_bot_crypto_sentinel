from datetime import datetime
from sqlalchemy import ForeignKey, String,BigInteger,Float,DateTime,Boolean
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id:Mapped[int]=mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False,index=True)
    username:Mapped[str]=mapped_column(String(32), nullable=True)
    language:Mapped[str]=mapped_column(String(2), default="en",server_default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    alerts:Mapped[List["Alerts"]]=relationship(back_populates="user", cascade="all, delete-orphan")

class Alerts(Base):
    __tablename__= "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user_account.tg_id', ondelete="CASCADE"))
    symbol: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    target_price: Mapped[float] = mapped_column(Float, nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user: Mapped["User"] = relationship(back_populates="alerts")