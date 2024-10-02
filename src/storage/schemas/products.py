from pydantic import BaseModel, ConfigDict, condecimal, conint


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: condecimal(gt=0, max_digits=10, decimal_places=2)


class ProductRequest(ProductBase):
    stock_quantity: conint(ge=0)


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    stock_quantity: conint(ge=0)
    id: int


class ProductItemsInfoResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int


class ProductUpdateResponse(BaseModel):
    detail: str | None = "Product updated successfuly"


class ProductDeleteResponse(BaseModel):
    detail: str | None = "Product deleted successfully"
