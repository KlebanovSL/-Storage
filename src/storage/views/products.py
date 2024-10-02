from src.database import SessionDep
from src.storage.models.products import Product
from src.storage.exceptions import (ProductNotFoundHTTPException,
                                    ProductIDsNotFoundHTTPException,
                                    ProductsOutOffStockHTTPException,
                                    )

from fastapi import Depends
from typing import Annotated, List
from sqlalchemy import (
    select, Select, update, Update,
    delete, Delete, Result, func, and_, or_
)


class ProductAPIView():

    def __init__(self, session: SessionDep):
        self.session = session

    async def create_product(self, data: dict) -> Product:
        product = Product(**data)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product

    async def get_products(self) -> List[Product]:
        query: Select = select(Product)
        result: Result = await self.session.execute(query)
        products = result.scalars().all()

        return products

    async def get_product(self, id: int) -> Product:
        query: Select = (
            select(Product)
            .where(Product.id == id)
        )
        result: Result = await self.session.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise ProductNotFoundHTTPException()

        return product

    async def update_product(self, id: int, data: dict) -> dict:
        stmt: Update = (
            update(Product)
            .where(Product.id == id)
            .values(**data)
        )
        result: Result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount == 0:
            raise ProductNotFoundHTTPException()

        return dict()

    async def delete_product(self, id: int) -> dict:
        stmt: Delete = (
            delete(Product)
            .where(Product.id == id)
        )
        result: Result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount == 0:
            raise ProductNotFoundHTTPException()

        return dict()


class ProductAPIViewMixin():

    async def validate_ids_exists(
        self, ids_list: list[int]
    ) -> None:
        query: Select = (
            select(func.count())
            .filter(Product.id.in_(ids_list))
        )
        result: Result = await self.session.execute(query)
        count = result.scalar()

        if count != len(ids_list):
            raise ProductIDsNotFoundHTTPException()

    async def validate_items_quantity(self, data: dict[int, int]) -> None:
        ids_list = list(data.keys())

        conditions = [
            and_(Product.id == product_id, Product.stock_quantity >= quantity)
            for product_id, quantity in data.items()
        ]
        query: Select = (
            select(func.count())
            .filter(or_(*conditions))
        )
        result: Result = await self.session.execute(query)
        count = result.scalar()

        if count != len(ids_list):
            raise ProductsOutOffStockHTTPException()


ProductAPIViewDep = Annotated[ProductAPIView, Depends(ProductAPIView)]
