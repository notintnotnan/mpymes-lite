from typing import List
from datetime import datetime

from sqlalchemy import ForeignKey, Enum, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.enums import AccountTypes, MovementTypes
from app.schemas.base import Base

class Business(Base):
    __tablename__ = "business_main"

    name:Mapped[str] = mapped_column(String, index=True)
    identifier:Mapped[str] = mapped_column(String,nullable=True)

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(), nullable=True)

    accounts:Mapped[List[Account]]  = relationship(back_populates='business')

class Account(Base):
    __tablename__ = "business_account"

    number:Mapped[str] = mapped_column(String, index=True)
    business_id:Mapped[int] = mapped_column(ForeignKey("business_main.id"))
    account_type:Mapped[str] = mapped_column(Enum(AccountTypes))

    business:Mapped[Business] = relationship(back_populates="accounts")
    movements:Mapped[List[Movement]] = relationship(back_populates="account") 

class MovementCategory(Base):
    __tablename__ = "business_movement_category"

    description:Mapped[str] = mapped_column(String)
    movement_type:Mapped[str] = mapped_column(Enum(MovementTypes))

class Movement(Base):
    __tablename__ = "business_movement"

    net_value:Mapped[float] = mapped_column(Numeric(scale=3))
    movement_type:Mapped[str] = mapped_column(Enum(MovementTypes))
    movement_category_id:Mapped[int] = mapped_column(ForeignKey("business_movement_category.id"))
    account_id:Mapped[int] = mapped_column(ForeignKey("business_account.id"))

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(), nullable=True)

    movement_category:Mapped[MovementCategory] = relationship()
    account:Mapped[Account] = relationship(back_populates="movements")

    @hybrid_property
    def value(self) -> float:
        return -1*self.net_value if self.movement_type == MovementTypes.DEBIT else self.net_value