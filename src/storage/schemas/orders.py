from enum import Enum
from datetime import datetime

from pydantic import BaseModel, conint, field_validator, ConfigDict

from src.storage.exceptions import DuplicateIDsHTTPException
from src.storage.schemas.products import ProductItemsInfoResponse


class OrderStatus(str, Enum):
    in_progress = "in progress"
    sent = "sent"
    delivered = "delivered"


class OrderItemRequest(BaseModel):
    product_id: conint(gt=0)
    quantity: conint(gt=0)


class OrderCreateRequest(BaseModel):
    items: list[OrderItemRequest]

    @field_validator("items")
    @classmethod
    def validate_unique_product_ids(cls, items):
        product_ids = [item.product_id for item in items]

        if len(product_ids) != len(set(product_ids)):
            raise DuplicateIDsHTTPException()

        return items

    def to_dict(self) -> dict[int, int]:
        return {item.product_id: item.quantity for item in self.items}


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    status: OrderStatus


class OrderItemsInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    quantity: conint(gt=0)
    product: ProductItemsInfoResponse


class OrderInfoResponse(OrderResponse):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    order_items: list[OrderItemsInfoResponse]


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus = OrderStatus.in_progress
