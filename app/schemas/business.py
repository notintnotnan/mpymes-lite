from typing import List
from datetime import datetime

from sqlalchemy import Column, Table, ForeignKey, Enum, String, Numeric, DateTime, func, select
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

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    business:Mapped[Business] = relationship(back_populates="accounts")
    movements:Mapped[List[Movement]] = relationship(back_populates="account")

class Tax(Base):
    __tablename__ = "business_tax"

    description:Mapped[str] = mapped_column(String)
    rate:Mapped[float] = mapped_column(Numeric(scale=6))

class MovementCategory(Base):
    __tablename__ = "business_movement_category"

    description:Mapped[str] = mapped_column(String)
    movement_type:Mapped[str] = mapped_column(Enum(MovementTypes))

movement_taxes = Table(
    "business_movement_taxes",
    Base.metadata,
    Column("tax_id", ForeignKey("business_tax.id")),
    Column("movement_id", ForeignKey("business_movement.id"))
)

class Movement(Base):
    # TODO: Implement discounts on value and tax calculations
    __tablename__ = "business_movement"

    base_value:Mapped[float] = mapped_column(Numeric(scale=3))
    movement_type:Mapped[str] = mapped_column(Enum(MovementTypes))
    movement_category_id:Mapped[int] = mapped_column(ForeignKey("business_movement_category.id"))
    account_id:Mapped[int] = mapped_column(ForeignKey("business_account.id"))

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(), nullable=True)

    movement_category:Mapped[MovementCategory] = relationship()
    account:Mapped[Account] = relationship(back_populates="movements")
    taxes:Mapped[List[Tax]] = relationship(secondary=movement_taxes)

    @hybrid_property
    def all_taxes(self):
        return self.taxes

    @all_taxes.expression
    def all_taxes(cls):
        return (
            select(movement_taxes.c.tax_id)
            .where(movement_taxes.c.movement_id == cls.id)
            .scalar_subquery()
        )

    @hybrid_property
    def total_taxes(self):
        return sum(tax.rate * self.base_value for tax in self.taxes)

    @total_taxes.expression
    def total_taxes(cls):
        return (
            select(func.coalesce(func.sum(Tax.rate) * cls.basevalue,0))
            .join(movement_taxes, movement_taxes.c.tax_id == Tax.id)
            .where(movement_taxes.c.movement_id == cls.id)
            .scalar_subquery()
        )

    @hybrid_property
    def total_value(self):
        return self.base_value + self.total_taxes

    @total_value.expression
    def total_value(cls):
        return cls.base_value + cls.total_taxes
