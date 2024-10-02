from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text, CheckConstraint

from src.database import Base
from src.storage.schemas.orders import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        server_onupdate=text("TIMEZONE('utc', now())"),
    )
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.in_progress
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete"
    )


class OrderItem(Base):
    __tablename__ = "orderitems"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    quantity: Mapped[int]
    order: Mapped["Order"] = relationship(
        back_populates="order_items"
    )
    product: Mapped["Product"] = relationship(  # noqa
        back_populates="order_items"
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="quantity should be greater than 0"
        ),
    )
