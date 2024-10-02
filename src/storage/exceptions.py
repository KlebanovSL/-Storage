from fastapi import HTTPException, status


class ProductNotFoundHTTPException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product not found"

    def __init__(self):
        ...


class DuplicateIDsHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Product IDs must be unique"

    def __init__(self):
        ...


class ProductIDsNotFoundHTTPException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "One or more product IDs were not found"

    def __init__(self):
        ...


class OrderNotFoundHTTPException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order not found"

    def __init__(self):
        ...


class ProductsOutOffStockHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "One or more products are not in the required quantity"

    def __init__(self):
        ...
