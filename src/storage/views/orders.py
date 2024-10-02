from src.database import SessionDep
from src.storage.views.products import ProductAPIViewMixin
from src.storage.models.orders import Order, OrderItem
from src.storage.exceptions import OrderNotFoundHTTPException

from fastapi import Depends
from sqlalchemy import select, Select, Result, update, Update, text
from sqlalchemy.orm import selectinload

from typing import Annotated


class OrderAPIView(ProductAPIViewMixin):

    def __init__(self, session: SessionDep):
        self.session = session

    async def create_order_with_items(self, data: dict):
        ids_list = list(data.keys())

        await self.validate_ids_exists(ids_list)
        await self.validate_items_quantity(data)
        order = Order()
        order_items = [
            OrderItem(
                product_id=product_id,
                quantity=quantity)
            for product_id, quantity in data.items()
        ]

        order.order_items.extend(order_items)

        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)

        return order

    async def get_orders(self) -> list[Order]:
        query: Select = select(Order)
        result: Result = await self.session.execute(query)
        orders = result.scalars().all()

        return orders

    async def get_order_info(self, id: int) -> Order:
        query: Select = (
            select(Order)
            .options(
                selectinload(Order.order_items)
                .load_only(OrderItem.quantity)
                .joinedload(OrderItem.product)
            )
            .filter_by(id=id)
        )
        result: Result = await self.session.execute(query)
        order = result.unique().scalar_one_or_none()

        return order

    async def update_order_status(self, id: int, data: dict) -> dict:
        stmt: Update = (
            update(Order)
            .where(Order.id == id)
            .values(
                **data,
                updated_at=text("TIMEZONE('utc', now())")
            )
        )
        result: Result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount == 0:
            raise OrderNotFoundHTTPException()

        return dict(detail="Order updated successfuly")


OrderAPIViewDep = Annotated[OrderAPIView, Depends(OrderAPIView)]
