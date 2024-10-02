from sqlalchemy import Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from decimal import Decimal

from src.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2)
    )
    stock_quantity: Mapped[int]
    order_items: Mapped[list["OrderItem"]] = relationship(  # noqa
        back_populates="product"
    )

    __table_args__ = (
        CheckConstraint(
            "stock_quantity >= 0",
            name="stock_quantity should be greater than 0"
        ),
    )
