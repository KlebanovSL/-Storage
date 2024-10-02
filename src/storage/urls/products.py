from fastapi import APIRouter, status, Path

from src.storage.schemas.products import (
    ProductRequest, ProductResponse,
    ProductUpdateResponse, ProductDeleteResponse
)
from src.storage.views.products import ProductAPIViewDep
from src.storage.schemas.swagger import ProductNotFoundModel


router = APIRouter()


@router.post(
    "/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_product(payload: ProductRequest, view: ProductAPIViewDep):
    return await view.create_product(payload.model_dump())


@router.get(
    "/", response_model=list[ProductResponse]
)
async def get_products(view: ProductAPIViewDep):
    return await view.get_products()


@router.get(
    "/{id}/",
    responses={
        status.HTTP_404_NOT_FOUND: dict(model=ProductNotFoundModel)
    },
    response_model=ProductResponse
)
async def get_product(view: ProductAPIViewDep, id: int = Path(ge=1)):
    return await view.get_product(id)


@router.put(
    "/{id}/",
    responses={
        status.HTTP_404_NOT_FOUND: dict(model=ProductNotFoundModel)
    },
    response_model=ProductUpdateResponse
)
async def update_product(
    payload: ProductRequest,
    view: ProductAPIViewDep,
    id: int = Path(ge=1)
):
    return await view.update_product(id, payload.model_dump())


@router.delete(
    "/{id}",
    responses={
        status.HTTP_404_NOT_FOUND: dict(model=ProductNotFoundModel)
    },
    response_model=ProductDeleteResponse
)
async def delete_product(id: int, view: ProductAPIViewDep):
    return await view.delete_product(id)
