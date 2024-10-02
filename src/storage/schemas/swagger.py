from pydantic import BaseModel

from src.storage.exceptions import (
    DuplicateIDsHTTPException,
    ProductIDsNotFoundHTTPException,
    ProductNotFoundHTTPException
)


class DuplicateIDsModel(BaseModel):
    detail: str = DuplicateIDsHTTPException.detail


class ProductIDsNotFoundModel(BaseModel):
    detail: str = ProductIDsNotFoundHTTPException.detail


class ProductNotFoundModel(BaseModel):
    detail: str = ProductNotFoundHTTPException.detail
