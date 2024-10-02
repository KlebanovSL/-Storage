from fastapi import APIRouter, status, Path

from src.storage.views.orders import OrderAPIViewDep
from src.storage.schemas.orders import (
    OrderCreateRequest, OrderResponse,
    OrderInfoResponse, OrderStatusUpdateRequest
                                        )
from src.storage.schemas.swagger import (
    DuplicateIDsModel, ProductIDsNotFoundModel
                                        )

router = APIRouter()


@router.post(
    "/",
    responses={
        status.HTTP_400_BAD_REQUEST: dict(model=DuplicateIDsModel),
        status.HTTP_404_NOT_FOUND: dict(model=ProductIDsNotFoundModel)
    },
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_order(payload: OrderCreateRequest, view: OrderAPIViewDep):
    return await view.create_order_with_items(payload.to_dict())


@router.get(
    "/",
    response_model=list[OrderResponse]
)
async def get_orders(view: OrderAPIViewDep):
    return await view.get_orders()


@router.get(
    "/{id}/",
    response_model=OrderInfoResponse
)
async def get_order_info(view: OrderAPIViewDep, id: int = Path(ge=1)):
    return await view.get_order_info(id)


@router.patch(
    "/{id}/status/"
)
async def update_order_status(
    view: OrderAPIViewDep,
    status: OrderStatusUpdateRequest,
    id: int = Path(ge=1)
):
    return await view.update_order_status(id, status.model_dump())
